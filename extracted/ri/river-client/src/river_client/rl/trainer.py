"""Async RL composition over Model.forward[_backward] and Model.optim_step."""

from __future__ import annotations

import asyncio
import copy
import dataclasses
import inspect
import math
import signal
import time
import warnings
from concurrent.futures import ThreadPoolExecutor
from contextlib import nullcontext
from dataclasses import dataclass
from datetime import timedelta
from functools import partial
from typing import Literal


from river_client.client import (
    Model,
    _ForwardBackwardNeedsSubBatches,
    _merge_forward_backward_sub_batch_results,
)
from river_client.types import Checkpoint, RiverError

from .advantages import (
    Batchwise,
    GroupCentered,
    _build_batch,
    _decouple,
    _rollout_counts,
    _training_rewards,
    accumulation_scale,
)
from .batch import TrainingBatch, _Build, _Item
from .spill import Spill, resolve_spill, scratch_spill
from .checkpoint import (
    Checkpointing,
    StateStore,
    fingerprint,
    row_order_fingerprint,
    training_plan_fingerprint,
)
from .config import (
    Adam,
    Admission,
    ForwardBackwardBatch,
    GroupCompletion,
    Truncation,
    _integer,
    acknowledge_risk,
)
from .custom_loss import custom_batch, loss_contract
from .engine import (
    call,
    group_from_state,
    group_state,
    trajectory_capture,
    trajectory_spill,
)
from .env import Env
from .losses import (
    CISPO,
    PPO,
    CustomLoss,
    ImportanceSampling,
    PolicyGradient,
    _positive,
    resolve_loss,
)
from .metrics import Metrics, MetricsReporter
from .progress import Activities
from .streaming_custom_loss import StreamingCustomLoss
from .trajectory import Trajectory, decode_state


@dataclass
class Step:
    """Result of one completed training batch.

    Attributes:
        n: Number of batches completed by this trainer.
        model_step: Number of optimizer updates applied to the model. A batch
            with no usable training data advances ``n`` but not ``model_step``.
        metrics: Training metrics for this batch, plus sampling activity since
            the previous result. Sampling metrics include work on other groups
            admitted ahead of this batch.
        trajectories: Trajectories selected for this batch.
    """

    n: int
    model_step: int
    # Sampling metrics cover work since the preceding emitted Step, including
    # async lookahead; they are not attributed to this batch's trajectories.
    metrics: dict[str, float]
    trajectories: list


def _sampling_interval(current, previous):
    """Non-overlapping sampling intervals, including work while the caller logs."""
    metrics = {
        f"sampling/{key}": float(current[key] - previous[key])
        for key in (
            "requests",
            "prompts",
            "submitted_requests",
            "submit_seconds",
            "generated_tokens",
            "prompt_tokens",
            "cached_prompt_tokens",
            "kv_refreshes",
            "queue_seconds",
            "request_seconds",
        )
    }
    metrics.update(
        {
            f"sampling/{key}": float(current[key])
            for key in ("inflight_requests", "inflight_prompts", "ready_prompts")
        }
    )
    elapsed = current["elapsed_seconds"] - previous["elapsed_seconds"]
    metrics["sampling/interval_seconds"] = elapsed
    if elapsed > 0:
        metrics["sampling/generated_tokens_per_second"] = (
            metrics["sampling/generated_tokens"] / elapsed
        )
    prompt_tokens = metrics["sampling/prompt_tokens"]
    if prompt_tokens > 0:
        metrics["sampling/cached_prompt_fraction"] = (
            metrics["sampling/cached_prompt_tokens"] / prompt_tokens
        )
    return metrics


def _require_finite_update(metrics, step):
    """Stop when the service reports a non-finite gradient norm for an update.

    The service has already applied the update, so its policy is corrupt: it
    must not be published for sampling (a non-finite adapter can crash shared
    inference workers), evaluated, or saved as a resume point. Raising before
    the journal records the update leaves saved trainer state at the previous
    step, so a restart resumes from the last finite policy. Services that
    report no gradient norm are not checked.
    """
    norm = metrics.get("grad_norm")
    if metrics.get("grad_norm_finite") == 0 or (
        isinstance(norm, (int, float)) and not math.isfinite(norm)
    ):
        raise FloatingPointError(
            f"optimizer step {step} reported a non-finite gradient norm; "
            "its policy was not published, evaluated or saved"
        )


def _callback_contract(callback):
    contract = getattr(callback, "contract", None)
    if callable(contract):
        return contract()
    return getattr(callback, "__qualname__", type(callback).__qualname__)


class SamplingExhausted(RiverError):
    """Dynamic sampling rejected too many groups to fill a training batch.

    Configured checkpoints are saved before this error reaches the caller.
    ``batch`` is the one-based training batch, and ``rejected`` counts rejected
    groups since the previous completed batch. To continue, resume with a larger
    ``DynamicSampling.max_attempted_group_ratio`` or a lower
    ``min_groups_per_step``. Persistent exhaustion usually means the data is too
    easy or too hard for the current policy, or the reward cannot separate
    samples; change the dataset or reward, or disable dynamic sampling.
    """

    def __init__(self, *, batch: int, rejected: int, limit: str):
        self.batch = batch
        self.rejected = rejected
        self._limit = limit
        super().__init__(
            f"dynamic_sampling exhausted {limit} before filling batch {batch} "
            f"({rejected} groups rejected); resume with a larger budget or lower "
            "min_groups_per_step, or revisit the dataset and reward"
        )

    def __reduce__(self):
        return (
            partial(
                type(self), batch=self.batch, rejected=self.rejected, limit=self._limit
            ),
            (),
            self.__dict__,
        )


class PolicyRewoundError(RiverError):
    """The server rewound a full-weight run to an earlier committed step.

    A full-weight RL run whose trainer crew restarts resumes from its newest
    auto checkpoint, and the updates after it are gone. Run the trainer again
    with the same :class:`Checkpointing` directory to resume from ``step``.
    """

    def __init__(self, step: int):
        super().__init__(
            f"the server rewound this run to optimizer step {step}, its newest "
            "auto checkpoint; run the trainer again with the same Checkpointing "
            "directory to resume from it"
        )
        self.step = step


_DEFAULT_TRUNCATION = Truncation()


def _resolve_metrics(metrics, log_step_metrics, metrics_interval):
    if log_step_metrics is None and metrics_interval is None:
        if metrics is None:
            return Metrics()
        if not isinstance(metrics, Metrics):
            raise TypeError("metrics must be an rl.Metrics")
        return metrics
    if metrics is not None:
        raise ValueError(
            "choose metrics or legacy log_step_metrics/metrics_interval, not both"
        )
    if log_step_metrics is not None and not isinstance(log_step_metrics, bool):
        raise TypeError("log_step_metrics must be a bool")
    if metrics_interval is not None:
        _positive(metrics_interval, "metrics_interval")
    metrics = Metrics(steps=bool(log_step_metrics), interval=metrics_interval)
    warnings.warn(
        "AsyncTrainer(log_step_metrics=..., metrics_interval=...) is deprecated and "
        "will be removed in a future river-client release; use metrics=rl.Metrics("
        f"steps={metrics.steps}, interval={metrics.interval!r}).",
        FutureWarning,
        stacklevel=3,
    )
    return metrics


class AsyncTrainer:
    """Train a model from rollout groups while sampling continues.

    Computes advantages from completed groups, submits forward/backward work,
    and applies optimizer updates. Set ``admission=Admission(max_staleness=0)`` to train
    synchronously or allow bounded policy lag for asynchronous training.
    Use one trainer to update a given model.
    """

    def __init__(
        self,
        *,
        engine,
        optimizer: Adam,
        completion: GroupCompletion,
        normalize: str | None = None,
        groups_per_step: int,
        group_size: int = 16,
        admission: Admission | None = None,
        advantage=None,
        loss: str
        | CustomLoss
        | CISPO
        | PPO
        | ImportanceSampling
        | PolicyGradient = "cispo",
        custom_loss_inputs=None,
        train_zero_advantage_batches: bool | None = None,
        max_staleness: int | None = None,
        stale_policy: str = "wait",
        allow_trajectory_loss: bool = False,
        allow_unbounded_staleness: bool = False,
        truncation: Truncation = _DEFAULT_TRUNCATION,
        checkpoint: Checkpointing | None = None,
        spill: Spill | bool | None = None,
        init_checkpoint=None,
        evaluator=None,
        run_config=None,
        max_importance_weight: float | None = None,
        routing_replay: bool = False,
        repeat_dataset: bool = True,
        batch_order: str = "completion",
        validate_batch=None,
        dataset_scheduler=None,
        forward_backward_groups: int | None = None,
        forward_backward_batch: ForwardBackwardBatch | Literal["auto"] | None = "auto",
        max_pending_forward_backward: int = 16,
        metrics: Metrics | None = None,
        log_step_metrics: bool | None = None,
        metrics_interval: float | None = None,
        **loss_config,
    ):
        """Configure reward processing, policy age, and optimizer updates.

        Args:
            engine: Rollout engine sharing the training model.
            optimizer: Optimizer settings for each update.
            completion: When a rollout group can be consumed.
            normalize: Legacy loss scaling for string-based objectives. Configured
                losses own this setting; omit it when passing rl.CISPO, rl.PPO,
                rl.PolicyGradient, or another configured loss. CustomLoss defaults
                to sum because its graph owns reduction. Choices are "token", "prompt",
                "sequence", "batch", or "sum". Prompt normalization averages trainable
                tokens within each reward group, then averages nonempty groups.
                Custom losses require ``"sum"`` and own their
                reduction; advantages are not rescaled by token/sequence counts.
            groups_per_step: Reward groups consumed per training batch.
            group_size: Samples requested for each dataset row.
            admission: Trainer-owned staleness, lookahead, oversampling, and
                optional DynamicSampling policy. Requires GroupCentered and wait
                completion/staleness when dynamic sampling is enabled.
                DynamicSampling.max_attempted_group_ratio can increase on resume.
            advantage: Advantage estimator; defaults to ``GroupCentered()``.
            loss: A configured rl.CISPO, rl.PolicyGradient, rl.PPO,
                rl.DecoupledPPO, rl.ImportanceSampling, or rl.CustomLoss. A bare
                river.CustomLoss also accepts the standard RL inputs.
                Existing string names "cispo", "ppo", "importance_sampling",
                and "decoupled_ppo" remain supported. The trainer prepares custom
                losses before rollouts.
                Custom losses default to one logical request per update. Explicit
                backward batching preserves each example's reductions and scalar
                operations. With batch-standardized advantages, each output must
                scale proportionally with the advantages or be independent of them.
                For other objectives, use group-local or no advantage
                standardization, or disable backward overlap.
                Deferred scaling changes floating-point rounding; numerically
                sensitive objectives should be compared against full-batch runs.
                Server microbatching and loss chunking still apply. Custom policy losses
                must apply sampling temperature themselves (for example, CE on
                ``logits / engine.temperature``); no implicit logit scaling occurs.
            custom_loss_inputs: Legacy alternative to rl.CustomLoss.input_adapter.
                Optional custom-loss callback taking a datum with
                loss_data (targets, old_logprobs, advantages, mask) and returning
                the declared loss_data columns. Apply mask to every loss term;
                it excludes prompt, image, tool and terminal positions and applies
                the configured staleness policy. For
                checkpointing, the callback must implement contract(), returning
                JSON-serializable configuration/version metadata.
                Runs on a worker thread; synchronize access to shared mutable state.
                With streaming backward, columns must match complete-batch
                construction, apart from batch advantage scaling. The trainer
                checks this before the optimizer.
            train_zero_advantage_batches: CustomLoss only: update even when every
                advantage is zero, for objectives with auxiliary training terms.
                Otherwise such batches skip backward and the optimizer. Mixed
                batches retain all masked tokens to preserve global reductions.
            max_staleness: Deprecated policy-age limit (default 2); use
                Admission.max_staleness. Zero gives synchronous admission.
            stale_policy: ``"wait"`` holds complete groups within the bound;
                ``"mask_span"`` masks old spans; ``"keep"`` ignores the bound.
            allow_trajectory_loss: Acknowledge options that may drop or fully
                mask trajectories.
            allow_unbounded_staleness: Acknowledge ``stale_policy="keep"``.
            truncation: Reward or drop policy for truncated trajectories.
            checkpoint: Durable trainer-state checkpoint settings.
            spill: Keep span arrays of completed trajectories on disk instead
                of in memory, reading them back when needed. ``None`` spills
                into the checkpoint's run directory when ``checkpoint`` is set
                and keeps arrays in memory otherwise. ``False`` keeps them in
                memory; ``True`` or ``rl.Spill()`` spills into the run
                directory, which requires ``checkpoint``.
                ``rl.Spill(directory)`` spills without checkpointing, into
                scratch files under ``directory``.
            init_checkpoint: Optional starting weights checkpoint.
            evaluator: Optional checkpoint-based evaluation runner.
            run_config: Serializable recipe values checked on resume.
            max_importance_weight: Importance-ratio limit for decoupled PPO.
            routing_replay: Replay captured expert routing during training.
            repeat_dataset: Cycle dataset rows when more groups are needed.
            batch_order: Consume groups by ``"completion"`` or ``"admission"``.
            validate_batch: Optional callback before a full batch trains.
            dataset_scheduler: Optional durable row scheduler implementing contract(),
                row(index, rows), commit(batch, groups), state_dict() and
                load_state_dict(state). Commit is synchronous with batch state;
                it must validate all inputs before mutating and perform no I/O.
            forward_backward_groups: Submit forward/backward after this many
                ready groups; requires group-centered training with wait policies.
            forward_backward_batch: ``"auto"`` enables threshold-based
                submission when eligible; set a ``ForwardBackwardBatch`` or
                ``None`` explicitly to override.
            max_pending_forward_backward: Limit concurrent submitted operations.
            metrics: Opt-in River Console reporting; see ``rl.Metrics``.
                ``None`` (default) reports nothing automatically.
            log_step_metrics: Deprecated; use ``metrics=rl.Metrics(steps=...)``.
            metrics_interval: Deprecated; use ``metrics=rl.Metrics(interval=...)``.
            loss_config: Legacy numeric options for string-based losses, such as
                eps_max. Do not combine these with a configured loss object.
        """
        self._loss_binding = resolve_loss(
            loss,
            normalize=normalize,
            options=loss_config,
            input_adapter=custom_loss_inputs,
            train_zero_advantage_batches=train_zero_advantage_batches,
            max_importance_weight=max_importance_weight,
        )
        if engine.temperature <= 0 or not math.isfinite(engine.temperature):
            raise ValueError(
                "RL training requires a finite positive sampling temperature"
            )
        _integer(max_pending_forward_backward, "max_pending_forward_backward", 1)
        self.max_pending_forward_backward = max_pending_forward_backward
        self.metrics = _resolve_metrics(metrics, log_step_metrics, metrics_interval)
        _integer(groups_per_step, "groups_per_step", 1)
        _integer(group_size, "group_size", 1)
        self._uses_admission = admission is not None
        if admission is not None:
            if not isinstance(admission, Admission):
                raise TypeError("admission must be an Admission")
            if any(
                value is not None
                for value in (
                    max_staleness,
                    engine.schedule.admit_ahead,
                    engine.schedule.oversample_factor,
                )
            ):
                raise ValueError(
                    "choose admission or legacy admission options, not both"
                )
            max_staleness = admission.max_staleness
            self._fingerprint_ahead = admission.batches_ahead
            self._fingerprint_oversample = admission.oversample
        else:
            # Compatibility for existing callers and checkpoints. Keep the old
            # clamp and serialized value only on this legacy path.
            warn_staleness = max_staleness is not None
            max_staleness = 2 if max_staleness is None else max_staleness
            ahead = (
                2
                if engine.schedule.admit_ahead is None
                else engine.schedule.admit_ahead
            )
            oversample = (
                1.0
                if engine.schedule.oversample_factor is None
                else engine.schedule.oversample_factor
            )
            _integer(max_staleness, "max_staleness")
            self._fingerprint_ahead = ahead
            self._fingerprint_oversample = oversample
            admission = Admission(
                max_staleness=max_staleness,
                ahead=min(ahead, max_staleness),
                oversample=oversample,
            )
            if warn_staleness:
                warnings.warn(
                    "AsyncTrainer(max_staleness=...) is deprecated and will be removed "
                    "in a future river-client release; use admission=rl.Admission("
                    f"max_staleness={max_staleness}, ahead={admission.batches_ahead}, "
                    f"oversample={admission.oversample}) and remove Schedule.admit_ahead/"
                    "oversample_factor to preserve admission behavior.",
                    FutureWarning,
                    stacklevel=2,
                )
        self.admission = admission
        dynamic_sampling = admission.dynamic_sampling is not None
        _integer(max_staleness, "max_staleness")
        if (
            groups_per_step < 1
            or group_size < completion.min_members
            or max_staleness < 0
        ):
            raise ValueError("invalid batch size, group quorum, or staleness limit")
        if stale_policy not in {"wait", "mask_span", "keep"}:
            raise ValueError("stale_policy must be wait, mask_span or keep")
        for name, value in (
            ("routing_replay", routing_replay),
            ("repeat_dataset", repeat_dataset),
        ):
            if type(value) is not bool:
                raise TypeError(f"{name} must be a boolean")
        if batch_order not in {"completion", "admission"}:
            raise ValueError("batch_order must be completion or admission")
        if (
            not repeat_dataset or batch_order == "admission"
        ) and stale_policy != "wait":
            raise ValueError(
                "finite datasets and admission ordering require stale_policy='wait'"
            )
        if routing_replay and not engine.return_expert_routing:
            raise ValueError(
                "routing_replay requires engine return_expert_routing=True"
            )
        if routing_replay and self._loss_binding.requires_proximal_forward:
            raise ValueError(
                "routing_replay is not supported for objectives with a proximal "
                "forward pass: forward-only requests do not support forced routing replay"
            )
        self.routing_replay, self.repeat_dataset, self.batch_order = (
            routing_replay,
            repeat_dataset,
            batch_order,
        )
        self.advantage = advantage if advantage is not None else GroupCentered()
        self.dynamic_sampling = dynamic_sampling
        if dynamic_sampling:
            if (
                type(self.advantage) is not GroupCentered
                or completion.mode != "wait"
                or stale_policy != "wait"
            ):
                raise ValueError(
                    "dynamic_sampling requires GroupCentered and wait completion/staleness"
                )
            if group_size < 2:
                raise ValueError("dynamic_sampling requires group_size >= 2")
            if dataset_scheduler is not None:
                raise ValueError("dynamic_sampling does not support dataset_scheduler")
            if self._loss_binding.train_zero_advantage_batches:
                raise ValueError(
                    "dynamic_sampling cannot discard groups used by "
                    "train_zero_advantage_batches"
                )
            floor = admission.dynamic_sampling.min_groups_per_step
            if floor is not None and floor > groups_per_step:
                raise ValueError("min_groups_per_step cannot exceed groups_per_step")
        if forward_backward_batch == "auto":
            eligible = (
                not self._loss_binding.is_custom
                and stale_policy == "wait"
                and completion.mode == "wait"
                and type(self.advantage) is GroupCentered
                # Preserve full-batch validation before worker mutations unless
                # the caller explicitly opts into overlapped computation.
                and validate_batch is None
            )
            forward_backward_batch = (
                ForwardBackwardBatch()
                if eligible and forward_backward_groups is None
                else None
            )
        if forward_backward_batch is not None and not isinstance(
            forward_backward_batch, ForwardBackwardBatch
        ):
            raise TypeError("forward_backward_batch must be a ForwardBackwardBatch")
        if forward_backward_batch is not None and forward_backward_groups is not None:
            raise ValueError(
                "choose forward_backward_batch or forward_backward_groups, not both"
            )
        self.forward_backward_batch = forward_backward_batch
        self._overlap = (
            forward_backward_groups is not None or forward_backward_batch is not None
        )
        self._streaming_custom_loss = None
        if forward_backward_groups is not None:
            _integer(forward_backward_groups, "forward_backward_groups", 1)
            if forward_backward_groups > groups_per_step:
                raise ValueError(
                    "forward_backward_groups cannot exceed groups_per_step"
                )
        if self._overlap:
            if stale_policy != "wait" or completion.mode != "wait":
                raise ValueError(
                    "streaming backward requires wait completion/staleness"
                )
            if type(self.advantage) is not GroupCentered:
                raise ValueError(
                    "streaming backward currently requires GroupCentered advantages"
                )
        self.forward_backward_groups = forward_backward_groups
        self._accumulating_groups = []
        self._prepared_groups = {}
        if self.normalize == "prompt" and completion.on_stragglers == "carry_over":
            raise ValueError(
                "prompt normalization does not support carry_over; splitting a "
                "prompt across updates would count each portion as a full prompt"
            )
        if completion.on_stragglers == "carry_over" and not isinstance(
            self.advantage, Batchwise
        ):
            raise ValueError(
                "carry_over requires Batchwise advantages; orphaned tails cannot be group-centered"
            )
        if (
            stale_policy == "wait"
            and completion.mode == "deadline"
            and completion.on_stragglers in {"carry_over", "discard"}
        ):
            raise ValueError(
                "stale_policy='wait' requires whole groups; partial-group completion "
                "requires an explicit mask_span or keep policy"
            )
        if max_staleness == 0 and (
            completion.on_stragglers == "carry_over" or self.admission.oversample != 1
        ):
            raise ValueError("synchronous admission cannot carry tails or oversample")
        for name, value in (
            ("allow_trajectory_loss", allow_trajectory_loss),
            ("allow_unbounded_staleness", allow_unbounded_staleness),
        ):
            if type(value) is not bool:
                raise TypeError(f"{name} must be a boolean")
        if stale_policy == "keep":
            acknowledge_risk(
                allow_unbounded_staleness,
                "allow_unbounded_staleness",
                "stale_policy='keep' does not enforce max_staleness; trajectories may train arbitrarily far off-policy.",
            )
        losses = []
        if stale_policy == "mask_span":
            losses.append(
                "pinned trajectories may be fully masked"
                if engine.sampling_policy == "trajectory"
                else "old segments or whole trajectories may be masked"
            )
        if completion.mode == "deadline" and completion.on_stragglers in {
            "discard",
            "truncate",
        }:
            losses.append(
                "group deadlines may discard or truncate long trajectories even when stale_policy='wait'"
            )
        if any(
            v in {"drop", "drop_and_exclude_from_baseline"}
            for v in (truncation.train, *truncation.by_cause.values())
        ):
            losses.append("truncation policy drops trajectory training data")
        if losses:
            acknowledge_risk(
                allow_trajectory_loss, "allow_trajectory_loss", "; ".join(losses) + "."
            )
        self.allow_trajectory_loss = allow_trajectory_loss
        self.allow_unbounded_staleness = allow_unbounded_staleness
        self.engine, self.optimizer, self.completion = engine, optimizer, completion
        self.groups_per_step, self.group_size = groups_per_step, group_size
        self.max_staleness, self.stale_policy, self.truncation = (
            max_staleness,
            stale_policy,
            truncation,
        )
        self.checkpoint, self.init_checkpoint, self.evaluator = (
            checkpoint,
            init_checkpoint,
            evaluator,
        )
        self.spill = spill
        self._spill_arrays, self._spill_directory = resolve_spill(spill, checkpoint)
        self._scratch = None
        self.dataset_scheduler = dataset_scheduler
        if dataset_scheduler is not None and (
            completion.mode != "wait" or stale_policy != "wait"
        ):
            raise ValueError(
                "dataset_scheduler requires complete groups and stale_policy=wait"
            )
        self.run_config = copy.deepcopy(run_config or {})
        if validate_batch is not None and not callable(validate_batch):
            raise TypeError("validate_batch must be callable")
        self.validate_batch = validate_batch
        self._loss_binding.bind(engine, checkpointing=checkpoint is not None)
        self._running = False
        self._status = "idle"
        self._dataset_exhausted = False
        self._backward_group_batches = []
        self._activities = Activities()

    # Existing attribute access delegates to the binding; it owns all loss state.
    @property
    def loss(self):
        return self._loss_binding.loss

    @property
    def loss_config(self):
        return self._loss_binding.config

    @property
    def normalize(self):
        return self._loss_binding.normalize

    @property
    def custom_loss_inputs(self):
        return self._loss_binding.input_adapter

    @property
    def train_zero_advantage_batches(self):
        return self._loss_binding.train_zero_advantage_batches

    @property
    def max_importance_weight(self):
        return self._loss_binding.max_importance_weight

    def progress(self):
        """Return current batch, model-update, and activity counters.

        ``model_step`` reports the last completed optimizer update, including
        while another update is in flight.
        """
        return {
            "status": self._status,
            "batches": getattr(self, "_n", 0),
            "backward_groups_completed": sum(
                count
                for count, indices in self._backward_group_batches
                if all(self._streamed_results[i] is not None for i in indices)
            ),
            "backward_chunks": len(getattr(self, "_streamed_chunks", ())),
            "pending_backward_requests": len(getattr(self, "_pending_backwards", ())),
            "model_step": getattr(self, "_committed_step", None),
            "pending_groups": len(getattr(self, "_pending", [])),
            "operations": self._activities.snapshot(),
            "rollouts": self.engine.progress(),
            **(
                {"checkpoint": copy.deepcopy(self._store.stats)}
                if getattr(self, "_store", None)
                else {}
            ),
        }

    async def _call(self, operation, function, *args, **kwargs):
        with self._activities.measure(operation):
            return await call(function, *args, **kwargs)

    async def _model_data(self, data):
        """Training data in the form the model takes.

        River's ``Model`` encodes a ``TrainingBatch`` datum by datum as it
        sends it. Other model adapters receive a list, built off the event
        loop.
        """
        if isinstance(data, TrainingBatch) and not isinstance(self.engine.model, Model):
            return await call(list, data)
        return data

    def _config(self):
        if self.optimizer.schedule is not None and not dataclasses.is_dataclass(
            self.optimizer.schedule
        ):
            raise ValueError(
                "checkpointed trainers require a serializable schedule such as rl.cosine()"
            )
        return {
            "optimizer": dataclasses.asdict(self.optimizer),
            "completion": dataclasses.asdict(self.completion),
            "budget": dataclasses.asdict(self.engine.budget),
            "sampling_policy": self.engine.sampling_policy,
            **(
                {"sampling_policy_selection": "latest_snapshot"}
                if self.engine._latest_snapshot_sampling
                else {}
            ),
            "kv_cache": dataclasses.asdict(self.engine.kv_cache),
            # Transport tuning does not change the rollout/training recipe.
            # Keep admission, priority and oversampling in the fingerprint.
            "schedule": {
                **{
                    key: value
                    for key, value in dataclasses.asdict(self.engine.schedule).items()
                    if key
                    not in {
                        "window",
                        "max_batch",
                        "max_batch_bytes",
                        "max_sample_requests",
                        "max_rpc_workers",
                    }
                },
                "admit_ahead": self._fingerprint_ahead,
                "oversample_factor": self._fingerprint_oversample,
            },
            "group_size": self.group_size,
            "groups_per_step": self.groups_per_step,
            # The budget ratio and batch floor only decide when sampling gives
            # up, so either may change on resume to continue an exhausted run.
            **({"dynamic_sampling": True} if self.dynamic_sampling else {}),
            # The filter changes which groups train, unlike the limits above.
            **(
                {"dynamic_sampling_keep": _callback_contract(keep)}
                if self.dynamic_sampling
                and (keep := self.admission.dynamic_sampling.keep) is not None
                else {}
            ),
            "normalize": self._loss_binding.normalize,
            "validate_batch": (
                None
                if self.validate_batch is None
                else self.validate_batch.__qualname__
            ),
            "routing_replay": self.routing_replay,
            "return_expert_routing": self.engine.return_expert_routing,
            **(
                {"top_logprobs": self.engine.top_logprobs}
                if self.engine.top_logprobs is not None
                else {}
            ),
            **(
                {"dataset_scheduler": self.dataset_scheduler.contract()}
                if self.dataset_scheduler is not None
                else {}
            ),
            "repeat_dataset": self.repeat_dataset,
            "batch_order": self.batch_order,
            # Checkpoint schema keys are stable across public option renames.
            "backward_groups": self.forward_backward_groups,
            **(
                {"backward_batch": dataclasses.asdict(self.forward_backward_batch)}
                if self.forward_backward_batch is not None
                else {}
            ),
            "advantage": {
                "type": type(self.advantage).__qualname__,
                **vars(self.advantage),
            },
            "loss": loss_contract(
                self._loss_binding.loss,
                self._loss_binding.input_adapter,
                requirements=self._loss_binding.requirements,
            )
            if self._loss_binding.is_custom
            else self._loss_binding.loss,
            **(
                {
                    "streaming_loss": loss_contract(
                        self._streaming_custom_loss.loss,
                        self._loss_binding.input_adapter,
                        requirements=self._loss_binding.requirements,
                    )
                }
                if self._streaming_custom_loss is not None
                else {}
            ),
            **(
                {
                    "train_zero_advantage_batches": self._loss_binding.train_zero_advantage_batches
                }
                if self._loss_binding.is_custom
                else {}
            ),
            "loss_config": self._loss_binding.config,
            "max_staleness": self.max_staleness,
            "stale_policy": self.stale_policy,
            "allow_trajectory_loss": self.allow_trajectory_loss,
            "allow_unbounded_staleness": self.allow_unbounded_staleness,
            "truncation": dataclasses.asdict(self.truncation),
            "seed": self.engine.seed,
            "temperature": self.engine.temperature,
            "top_p": self.engine.top_p,
            "top_k": self.engine.top_k,
            "renderer": type(self.engine.renderer).__qualname__,
            # Keep the original create_model selection in the durable recipe.
            # Canonical metadata must not invalidate existing fingerprints or
            # make new checkpoints unreadable by alias-based clients on rollback.
            "base_model": getattr(
                self.engine.model,
                "_requested_base_model",
                getattr(self.engine.model, "base_model", None),
            ),
            "max_importance_weight": self._loss_binding.max_importance_weight,
            "run_config": self.run_config,
            "environment": (
                type(self.engine.env).__qualname__
                if isinstance(self.engine.env, Env)
                else getattr(
                    self.engine.env, "__qualname__", type(self.engine.env).__qualname__
                )
            ),
            "evaluation": (
                None if self.evaluator is None else self.evaluator.config_dict()
            ),
        }

    def _image_session(self):
        model = self.engine.model
        session = getattr(model, "_session", getattr(model, "session", None))
        return session if callable(getattr(session, "restore_images", None)) else None

    def _compatible_config_fingerprints(self, config):
        compatible_fingerprints = self._loss_binding.compatible_fingerprints(config)
        if (
            self.engine._live_full_weight
            and config["sampling_policy"] == "segment"
            and config["kv_cache"]
            == {"max_staleness": 0, "on_limit": "refill", "allow_reprefill": True}
        ):
            # v0.17.0 named these defaults trajectory/hold, but full-weight
            # sampling already used live policies without retained KV.
            # Accept only that old spelling of the corrected defaults;
            # every other recipe field must still match, including the
            # existing equivalence rules for omitted/default loss options.
            compatible_fingerprints.update(
                self._loss_binding.compatible_fingerprints(
                    config
                    | {
                        "sampling_policy": "trajectory",
                        "kv_cache": {
                            "max_staleness": 0,
                            "on_limit": "hold",
                            "allow_reprefill": False,
                        },
                    }
                )
            )
        return compatible_fingerprints

    def _adopt_auto_checkpoint(self, latest, training_run_id):
        """Make ``latest``, run ``training_run_id``'s newest auto checkpoint,
        the recovery base when it is newer than the base.

        A post-load auto save refreshes an expiring source from another run.
        At equal steps, keep durable saves and that run's own saves.
        """
        if latest is not None and (
            self._base is None
            or latest.step > self._base.step
            or (
                not self._durable_base
                and latest.step == self._base.step
                and not self._base.path.startswith(f"river://{training_run_id}/")
                and latest.policy_version is not None
                and latest.policy_version == self._base.policy_version
            )
        ):
            self._base = latest
            self._durable_base = False

    async def _save_state(self, *, background=False):
        if self._state_write is not None:
            await self._wait_state_write(self._state_write)
        if self._full_weight:
            self._adopt_auto_checkpoint(
                await self._call(
                    "auto_checkpoint", self.engine.model.latest_auto_checkpoint
                ),
                self.engine.model.training_run_id,
            )
        # The previous write has committed, so only newer content is copied.
        capture = self._store.capture()
        state = {
            "version": 1,
            **self._fingerprints,
            "n": self._n,
            "submitted": self._submitted,
            # Retain the persisted key for checkpoints written by earlier clients.
            "dynamic_sampling_counts": self._dynamic_sampling_counts.copy(),
            "model_step": self.engine.model.step,
            "dataset_images": self._dataset_images,
            "sampling_schedule": {
                **dataclasses.asdict(self.engine.schedule),
                "admit_ahead": self._fingerprint_ahead,
                "oversample_factor": self._fingerprint_oversample,
            },
            "base": None if self._base is None else dataclasses.asdict(self._base),
            "durable_base": self._durable_base,
            "updates_since_save": self._updates_since_save,
            **(
                {
                    "training_run_id": self.engine.model.training_run_id,
                    # A new run reads this run's newest auto checkpoint by it.
                    "model_id": self.engine.model.model_id,
                    # Steps repeat after a rewind; only the id names the weights.
                    "policy_id": self._policy.id,
                }
                if self._full_weight
                else {}
            ),
            # Each committed update is written once and referenced afterwards,
            # by reference to the span records of the trajectories it trained.
            "journal": [capture.update(update) for update in self._journal],
            "admitted_policy_steps": self._admitted_policy_steps.copy(),
            "active": sorted(self._active),
            "finished": sorted(self._finished),
            "received": sorted(self._received),
            "pending": [group_state(g, capture.trajectory) for g in self._pending],
            **(
                {"accumulating_groups": self._accumulating_groups.copy()}
                if self._overlap and self.max_staleness > 0
                else {}
            ),
            "engine": await self._engine_state(capture),
            **(
                {"dataset_scheduler": self.dataset_scheduler.state_dict()}
                if self.dataset_scheduler is not None
                else {}
            ),
            "eval_history": (
                []
                if self.evaluator is None
                else copy.deepcopy(self.evaluator.state_dict())
            ),
        }
        session = self._image_session()
        images = session._client._local_images if session is not None else None

        async def persist():
            await self._call(
                "checkpoint_state",
                self._store.save,
                state,
                images=images,
                spills=capture.spills,
            )
            # Committed journal updates live in the checkpoint; keep only
            # references in memory and reload them if recovery replays them.
            # This also releases the trajectories an update's batches build from.
            self._journal = [self._store.release(update) for update in self._journal]
            self._saved_model_step = state["model_step"]
            self._last_state_save = time.monotonic()

        self._state_write = asyncio.create_task(persist())
        if not background:
            await self._wait_state_write(self._state_write)
        return self._state_write

    async def _engine_state(self, capture):
        token = trajectory_capture.set(capture.trajectory)
        spill = trajectory_spill.set(capture.spill)
        try:
            return await self.engine.state_dict()
        finally:
            trajectory_spill.reset(spill)
            trajectory_capture.reset(token)

    @staticmethod
    async def _wait_state_write(write):
        # Cancelling an await cannot stop the filesystem writer. Drain it before
        # another save or shutdown can replace metadata or prune its arrays.
        cancelled = None
        while not write.done():
            try:
                await asyncio.shield(write)
            except asyncio.CancelledError as error:
                cancelled = error
        write.result()
        if cancelled is not None:
            raise cancelled

    async def _refresh_policy(self):
        if self.engine.server_capabilities is not None:
            self.engine.server_capabilities.require("policy_versions_v1")
            if self._overlap and (
                self._loss_binding.normalize != "sum"
                or self.advantage.standardize == "batch"
            ):
                self.engine.server_capabilities.require("gradient_scale_v1")
        read = getattr(self.engine.model, "get_policy_version", None)
        self._policy = await call(read) if read is not None else None
        if read is not None and self._policy is None:
            raise RuntimeError(
                "RL requires a server with committed policy-version support"
            )

    def _policy_guard(self):
        policy = getattr(self, "_policy", None)
        return {} if policy is None else {"expected_policy_id": policy.id}

    def _apply_policy_provenance(self, trajectories):
        policy = getattr(self, "_policy", None)
        if policy is None:
            return
        for trajectory in trajectories:
            spans = []
            for span in trajectory.spans:
                if span.kind != "generated":
                    spans.append(span)
                    continue
                sampled = span.policy_version
                if sampled is None or sampled.lineage_id != policy.lineage_id:
                    raise RuntimeError(
                        "Sample is missing policy provenance or belongs to another lineage"
                    )
                age = policy.step - sampled.step
                if age < 0 or (
                    self.stale_policy == "wait" and age > self.max_staleness
                ):
                    raise RuntimeError(
                        "Sample policy violates the reserved staleness bound"
                    )
                policy_step = self.engine.model.step - age
                # Restamping shares the span's arrays, spilled ones included.
                spans.append(
                    span
                    if span.policy_step == policy_step
                    else span._with_policy_step(policy_step)
                )
            # Keep an unchanged span list: checkpoint saves and journaled
            # batches find a trajectory's committed records by its list.
            if any(new is not old for new, old in zip(spans, trajectory._spans)):
                trajectory._spans = spans

    async def _save_weights(self, *, durable=False):
        checkpoint = await self._call(
            "checkpoint_weights",
            self.engine.model.save_weights,
            f"rl-{self._run_key}-batch-{self._n:08d}",
            mode="training",
            durable=durable,
            **(
                {}
                if durable
                else {"ttl": timedelta(seconds=self.checkpoint.recovery_ttl_seconds)}
            ),
            **(
                {"immutable": True, **self._policy_guard()}
                if getattr(self, "_policy", None)
                else {}
            ),
        )
        if (
            checkpoint.step != self.engine.model.step
            or checkpoint.checkpoint_type != "training"
        ):
            raise ValueError(
                "saved training weights disagree with the trainer's model step"
            )
        self._base, self._journal = checkpoint, []
        self._durable_base = durable
        self._updates_since_save = 0
        await self._save_state()

    async def _publish_sampling_snapshot(self, *, recovering=False):
        if not self.engine._latest_snapshot_sampling:
            return
        step = self.engine.model.step
        if self._published_sampling_step == step:
            return
        # Called before new admissions, after committed training state is
        # recoverable. Full-weight publication also updates active trajectories.
        if self._store and not recovering and self._saved_model_step != step:
            await self._save_state()
        # A full-weight run pushes its weights to the run's own sampler and
        # stores nothing, so there is no snapshot version to keep. Other runs
        # keep each snapshot on NFS only, with no cloud copy.
        mode = "publish" if self._full_weight else "inference"
        storage = {} if self._full_weight else {"durable": False}
        immutable = {} if self._full_weight else {"immutable": True}
        checkpoint = await self._call(
            "sampling_snapshot",
            self.engine.model.save_weights,
            f"rl-{self._run_key}-sampling-{step:08d}",
            mode=mode,
            **storage,
            **({**immutable, **self._policy_guard()} if self._policy else {}),
        )
        if (
            checkpoint.step != step
            or checkpoint.checkpoint_type != mode
            or (self._policy is not None and checkpoint.policy_version != self._policy)
        ):
            raise RuntimeError(
                "published sampling snapshot does not match the committed policy"
            )
        self._published_sampling_step = step

    def _admit(self, row, group_id):
        group_id = self.engine.submit(
            row,
            group_size=self.group_size,
            completion=self.completion,
            id=group_id,
            priority=self._committed_step if self.stale_policy == "wait" else 0,
        )
        if self.stale_policy == "wait":
            self._admitted_policy_steps[group_id] = self._committed_step
        self._active.add(group_id)

    async def _resume_full_weight(self, saved):
        """Resume at the server's committed step, never the saved one (R56).

        The same run continues from the step the server committed, which is
        the newest auto checkpoint when its crew restarted. A new run loads
        the newest training checkpoint recorded before the restart, or keeps the
        weights it was created with if there was none. No update is replayed.
        When the resumed policy is not the saved one, every unconsumed group
        is sampled again from the resumed weights, so no sample from
        discarded weights is trained on. The batch counter is kept.

        Returns the groups to readmit (None when saved rollouts still apply)
        and whether the resumed weights need a replacement checkpoint. When
        readmitting, the caller must save the new state before any update, or
        a later resume could restore discarded rollouts. A required checkpoint
        must succeed before that state replaces the previous recovery base.
        """
        model = self.engine.model
        self._base = None if saved["base"] is None else Checkpoint(**saved["base"])
        same_run = saved["training_run_id"] == model.training_run_id
        if same_run:
            await call(model.sync_committed_policy)
        else:
            # The saved run can commit an auto checkpoint after the state was
            # saved, as when the driver dies during a step. Once that run ends
            # the server keeps only its newest, which may not be the saved base.
            # The server records auto checkpoints only of acknowledged updates,
            # never of one with a non-finite gradient norm. States written
            # before model_id was recorded cannot look it up.
            if "model_id" in saved:
                self._adopt_auto_checkpoint(
                    await self._call(
                        "auto_checkpoint",
                        model.latest_auto_checkpoint,
                        model_id=saved["model_id"],
                    ),
                    saved["training_run_id"],
                )
            if self._base is not None:
                await self._call(
                    "load_weights",
                    model.load_weights,
                    self._base,
                    load_optimizer=True,
                )
        await self._refresh_policy()
        self._committed_step = model.step
        if self._policy.id == saved["policy_id"]:
            return None, False
        checkpoint_recovery = False
        if (
            same_run
            and self._policy.parent_id == saved["policy_id"]
            and model.step > saved["model_step"]
        ):
            # An optimizer committed before the driver saved state. Its parent
            # proves forward progress: the saved base remains a valid ancestor.
            self._updates_since_save += model.step - saved["model_step"]
        else:
            # A new run loaded its base, so later updates were lost. In the
            # same run this could be multiple unsaved updates or a rewind.
            # Retain the old base until the caller checkpoints the resumed
            # weights; neither step nor lineage proves which branch survived.
            self._updates_since_save = 0
            checkpoint_recovery = same_run
        unconsumed = set(saved["active"]) | {g["id"] for g in saved["pending"]}
        engine = saved["engine"]
        rows = {
            g["id"]: g["row"]
            for g in (*engine["groups"], *engine["outbox"], *saved["pending"])
            if g["id"] in unconsumed
        }
        if rows.keys() != unconsumed:
            raise ValueError("resume is missing rows for unconsumed rollout groups")
        saved.update(
            active=[],
            pending=[],
            finished=sorted(set(saved["finished"]) - unconsumed),
            admitted_policy_steps={},
            accumulating_groups=[],
            engine={**engine, "groups": [], "outbox": []},
        )
        readmit = [
            (group_id, decode_state(rows[group_id]))
            for group_id in sorted(
                unconsumed, key=lambda group_id: int(group_id.rpartition("-")[2])
            )
        ]
        return readmit, checkpoint_recovery

    async def _raise_if_rewound(self, error):
        try:
            committed = await call(self.engine.model.get_policy_version)
        except Exception:
            # The original failure is the one to report.
            return
        if committed is not None and committed.step < self._committed_step:
            raise PolicyRewoundError(committed.step) from error

    async def _periodic_checkpoint(self):
        while True:
            interval = self.checkpoint.rollout_every
            await asyncio.sleep(
                max(0, self._last_state_save + interval - time.monotonic())
            )
            async with self._lock:
                # A required save may have completed while we waited for the lock.
                if time.monotonic() - self._last_state_save < interval:
                    continue
                write = await self._save_state(background=True)
            # The captured state owns its data. Group collection and backward
            # submission can continue while this ordered snapshot reaches disk.
            await self._wait_state_write(write)

    def _backward_kwargs(self, data, *, zero_out=True):
        routing = _routing(data)
        if self.routing_replay and any(
            not handle and not recovered for handle, recovered in routing
        ):
            raise ValueError(
                "routing_replay requires a routing handle for every training datum"
            )
        replay = self.routing_replay and all(handle for handle, _ in routing)
        if self.routing_replay and not replay:
            warnings.warn(
                "Recovered training data has no routing capture; this backward batch "
                "will use trainer-computed routing.",
                RuntimeWarning,
                stacklevel=2,
            )
        return {
            "loss_fn": (
                self._streaming_custom_loss.loss
                if self._streaming_custom_loss is not None
                else self._loss_binding.backward_loss
            ),
            "zero_out": zero_out,
            **(
                {"force_routing_replay": replay, "compute_expert_flip_metric": replay}
                if self.routing_replay
                else {}
            ),
            **self._loss_binding.config,
            **self._policy_guard(),
            **(
                {"allow_routing_fallback": True}
                if replay and any(recovered for _, recovered in routing)
                else {}
            ),
        }

    def _backward_data(self, data, *, preserve_recovery=False):
        missing = self.routing_replay and any(
            not handle for handle, _ in _routing(data)
        )
        if isinstance(data, TrainingBatch):
            return data.with_items(
                **({} if preserve_recovery else {"drop_recovery": True}),
                **({"drop_routing": True} if missing else {}),
            )
        return [
            {
                k: v
                for k, v in datum.items()
                if (preserve_recovery or k != "_rl_recovered_routing")
                and not (missing and k.startswith("expert_routing_"))
            }
            for datum in data
        ]

    async def _backward(self, data, *, zero_out=True):
        before = self.engine.model.step
        fb = await self._call(
            "backward",
            self.engine.model.forward_backward,
            await self._model_data(self._backward_data(data)),
            **self._backward_kwargs(data, zero_out=zero_out),
        )
        # Deliberately wait for successful backward before submitting Adam.
        # Model.train_step pipelines Adam even if backward subsequently fails.
        if self.engine.model.step != before:
            raise RuntimeError(
                "model step changed during backward; the trainer requires exclusive update ownership"
            )
        return fb

    async def _wait_backward(self, pending):
        with self._activities.measure("backward"):
            if inspect.iscoroutinefunction(pending.result):
                return await pending.result()
            if self._backward_executor is None:
                self._backward_executor = ThreadPoolExecutor(
                    max_workers=self.max_pending_forward_backward,
                    thread_name_prefix="rl-backward",
                )
            # RPC completion waits must not occupy the executor needed to
            # submit further groups or execute rollout environment tools.
            return await asyncio.get_running_loop().run_in_executor(
                self._backward_executor, pending.result
            )

    async def _collect_backwards(self, *, all_pending=False):
        while self._pending_backwards:
            index, task = self._pending_backwards[0]
            if not all_pending and not task.done():
                break
            self._streamed_results[index] = await asyncio.shield(task)
            self._pending_backwards.pop(0)
            self._check_step()
        # Surface an out-of-order failure without waiting for an earlier RPC.
        for index, task in self._pending_backwards:
            if task.done():
                task.result()

    async def _drain_backwards(self):
        # Accepted RPCs outlive cancellation of their waiter. Drain them before
        # closing the model, including when recovery fails before the main loop.
        drain = asyncio.gather(
            *(task for index, task in self._pending_backwards),
            return_exceptions=True,
        )
        cancelled = None
        while not drain.done():
            try:
                await asyncio.shield(drain)
            except asyncio.CancelledError as error:
                # Even repeated cancellation must wait for accepted work and
                # executor cleanup before recovery can close the model.
                cancelled = error
        results = drain.result()
        self._pending_backwards.clear()
        if self._backward_executor is not None:
            self._backward_executor.shutdown(wait=True)
            self._backward_executor = None
        if cancelled is not None:
            raise cancelled
        return next((r for r in results if isinstance(r, BaseException)), None)

    async def _submit_backward(self, data, group_count):
        first = len(self._streamed_results)
        if data:
            await self._submit_backward_chunk(data)
        # Register only after successful submission. Failed or cancelled
        # submissions cannot count their groups as completed.
        self._backward_group_batches.append(
            (group_count, range(first, len(self._streamed_results)))
        )

    async def _submit_backward_chunk(self, data, *, prepared=None):
        await self._collect_backwards()
        if len(self._pending_backwards) >= self.max_pending_forward_backward:
            await asyncio.shield(self._pending_backwards[0][1])
            await self._collect_backwards()
        zero_out = not self._streamed_chunks
        cancelled = None
        submit = getattr(self.engine.model, "submit_forward_backward", None)
        if submit is None:
            # Custom model adapters can still expose only the blocking method.
            result = await self._backward(data, zero_out=zero_out)
            self._streamed_results.append(result)
        else:
            if prepared is None:
                prepared = (
                    await self._model_data(self._backward_data(data)),
                    self._backward_kwargs(data),
                )
            request_data, request_kwargs = prepared
            # Await submission in order, not GPU completion: seq_id and the
            # initial gradient reset must precede every later contribution.
            submission = asyncio.create_task(
                self._call(
                    "backward_submit",
                    submit,
                    request_data,
                    **{**request_kwargs, "zero_out": zero_out},
                )
            )
            try:
                while not submission.done():
                    try:
                        await asyncio.shield(submission)
                    except asyncio.CancelledError as error:
                        # Even repeated cancellation must recover an accepted
                        # handle so finalization can drain its GPU work.
                        cancelled = error
                pending = submission.result()
            except _ForwardBackwardNeedsSubBatches as split:
                if cancelled is not None:
                    raise cancelled
                # Keep byte-sized uploads in the same bounded pipeline. Each
                # piece owns its result and replay data; only the first useful
                # piece of the update resets gradients. No optimizer is allowed
                # until every accepted piece completes successfully.
                # Drop ignored routing captures from replay data too, so a
                # smaller journal chunk cannot re-enable them after a restore.
                data = self._backward_data(data, preserve_recovery=True)
                for sub_batch in split.sub_batch_slices:
                    # Preserve batch-wide routing fallback and loss settings;
                    # repartitioning must not change the payload we measured.
                    await self._submit_backward_chunk(
                        data[sub_batch],
                        prepared=(request_data[sub_batch], request_kwargs),
                    )
                return
            index = len(self._streamed_results)
            self._streamed_results.append(None)
            task = asyncio.create_task(self._wait_backward(pending))
            self._pending_backwards.append((index, task))
        self._streamed_chunks.append(data)
        if cancelled is not None:
            raise cancelled

    async def _optimize(self, optimizer_kwargs):
        before = self.engine.model.step
        optim = await self._call(
            "optimizer",
            self.engine.model.optim_step,
            **optimizer_kwargs,
            **self._policy_guard(),
        )
        _require_finite_update(optim.metrics, before + 1)
        if getattr(self, "_policy", None) is not None:
            committed = optim.policy_version
            if (
                committed is None
                or committed.parent_id != self._policy.id
                or committed.step != self._policy.step + 1
            ):
                raise RuntimeError(
                    "Optimizer acknowledgement has an invalid committed policy"
                )
            self._policy = committed
        if self.engine.model.step != before + 1:
            raise RuntimeError(
                "optimizer completion did not advance the model by exactly one step"
            )
        return optim

    async def _update(self, data, optimizer_kwargs, *, chunks=None, recovering=False):
        if recovering:
            self._committed_step = self.engine.model.step
            # Journal data is restored even when its original trajectories were
            # fresh. Reuse captures where possible, with admission-time fallback.
            if chunks is None:
                data = _recovered(data)
            else:
                chunks = [_recovered(chunk) for chunk in chunks]
        if chunks is None:
            fb = await self._backward(data)
        else:
            self._streamed_groups = set()
            self._streamed_chunks, self._streamed_results = [], []
            self._backward_group_batches = []
            try:
                # Keep journal order and gradient reset, but overlap completion
                # waits using the same bounded pipeline as live accumulation.
                for chunk in chunks:
                    await self._submit_backward(chunk, 0)
                await self._collect_backwards(all_pending=True)
                fb = _merge_forward_backward_sub_batch_results(
                    self._streamed_results,
                    [len(c) for c in self._streamed_chunks],
                    custom=self._loss_binding.is_custom,
                )
            finally:
                await self._drain_backwards()
        return fb, await self._optimize(optimizer_kwargs)

    def _restore_update(self, update):
        """Rebuild a journal update stored by reference as training batches.

        Its recipes name each datum's trajectory, run, advantage and
        corrections; the current loss binding, which the resume fingerprint
        pins, supplies the rest. Updates journaled as datums pass through.
        """
        if "kind" not in update:
            return update
        sources = [
            Trajectory.from_state_dict(state)._datum_source()
            for state in update["trajectories"]
        ]
        binding = self._loss_binding
        builds = [
            _Build(
                current_step=build["current_step"],
                max_staleness=build["max_staleness"],
                requirements=binding.requirements if build["loss"] else None,
                include_loss_mask=build["include_loss_mask"],
                loss=binding if build["loss"] else None,
            )
            for build in update["builds"]
        ]
        rows = update["proximal"]
        chunks = []
        for chunk in update["chunks"]:
            batch = TrainingBatch(
                _Item(
                    source=sources[item["trajectory"]],
                    run=item["run"],
                    advantage=item["advantage"],
                    denominator=item["denominator"],
                    length=item["length"],
                    advantaged=item["advantaged"],
                    routing_handle=item["routing_handle"],
                    recovered=item["recovered"],
                    build=builds[item["build"]],
                    proximal=None
                    if item["proximal"] is None
                    else (rows[item["proximal"]], item["max_importance_weight"]),
                    drop_recovery=item["drop_recovery"],
                    drop_routing=item["drop_routing"],
                )
                for item in chunk["items"]
            )
            if chunk["custom"]:
                batch = custom_batch(batch, binding.loss, binding.input_adapter)
            chunks.append(batch)
        if update["kind"] == "data":
            return {"data": chunks[0], "optimizer": update["optimizer"]}
        return {"chunks": chunks, "optimizer": update["optimizer"]}

    async def _prepare_group(self, group, *, advantages=None):
        """Use the same masks, advantages and data conversion for filtering/backward."""
        estimator = self.advantage
        if estimator.standardize == "batch":
            estimator = dataclasses.replace(estimator, standardize=False)
        self._apply_policy_provenance(group.trajectories)
        data, metrics = await call(
            _build_batch,
            [group.trajectories],
            estimator=estimator,
            normalize=self._loss_binding.normalize,
            truncation=self.truncation,
            min_members=self.completion.min_members,
            current_step=self._committed_step,
            max_staleness=self.max_staleness,
            defer_normalization=True,
            advantages=advantages,
            include_loss_mask=self._loss_binding.is_custom,
            loss=self._loss_binding,
        )
        if metrics["staleness/frac_masked"]:
            raise RuntimeError(
                "backward accumulation received samples outside the staleness bound"
            )
        # Advantages align with input positions, including conditioning/image tokens.
        return data, sum(data.lengths())

    async def _accumulate_ready(self, *, flush=False):
        """Backprop complete groups; keep their trajectories pending until Adam.

        Checkpoints persist these pending groups, not worker gradients. After
        restoring weights we replay them with zero_out=True on the first useful
        chunk. A failed/uncertain backward never permits an optimizer operation.
        """
        if not self._overlap:
            return
        async with self._lock:
            while not self._stop.is_set():
                estimator = self.advantage
                if estimator.standardize == "batch":
                    estimator = dataclasses.replace(estimator, standardize=False)
                batch_groups = (
                    self._wait_accumulation_groups()
                    if self.max_staleness > 0
                    else self._pending
                )
                groups = [g for g in batch_groups if g.id not in self._streamed_groups]
                # Excluded members can force a group's baseline to use the
                # whole batch. Only these groups wait for the final rewards.
                if not flush:
                    groups = [
                        g
                        for g in groups
                        if sum(
                            value is not None
                            for value in _training_rewards(
                                [g.trajectories],
                                self.truncation,
                                estimator=estimator,
                                min_members=self.completion.min_members,
                            )[0]
                        )
                        >= self.completion.min_members
                    ]
                # Complete groups with local baselines are stable within an
                # update. Retain their token arrays while the threshold fills,
                # but never reuse preparations at another step or after a
                # reservation change removes a group from this selection.
                eligible = {(self._committed_step, g.id) for g in groups}
                self._prepared_groups = {
                    key: prepared
                    for key, prepared in self._prepared_groups.items()
                    if key in eligible
                }
                if not groups:
                    return
                starting_custom = (
                    self._streaming_custom_loss is not None
                    and not self._streamed_chunks
                    and not self._loss_binding.train_zero_advantage_batches
                )
                if self.forward_backward_batch is None:
                    if len(groups) < self.forward_backward_groups and not flush:
                        return
                    if not starting_custom:
                        groups = groups[: self.forward_backward_groups]
                if any(
                    not g.final or len(g.trajectories) != self.group_size
                    for g in groups
                ):
                    raise RuntimeError(
                        "streaming backward requires complete reward groups"
                    )
                by_id = None
                if flush:
                    all_values = estimator(
                        _training_rewards(
                            [g.trajectories for g in batch_groups],
                            self.truncation,
                            estimator=estimator,
                            min_members=self.completion.min_members,
                        ),
                        min_members=self.completion.min_members,
                    )
                    by_id = {
                        g.id: values
                        for g, values in zip(batch_groups, all_values, strict=True)
                    }
                self._check_step()
                # Prepared groups hold trajectory references, not datums.
                data, selected = TrainingBatch(), []
                tokens = 0
                for group in groups:
                    key = (self._committed_step, group.id)
                    if key not in self._prepared_groups:
                        self._prepared_groups[key] = await self._prepare_group(
                            group,
                            advantages=None if by_id is None else [by_id[group.id]],
                        )
                    contribution, input_tokens = self._prepared_groups[key]
                    if starting_custom and not contribution.advantaged():
                        continue
                    data += contribution
                    selected.append(group)
                    tokens += input_tokens
                    if (
                        self.forward_backward_batch is not None
                        and self.forward_backward_batch.reached(len(data), tokens)
                    ):
                        break
                    if (
                        self.forward_backward_batch is None
                        and len(selected) >= self.forward_backward_groups
                    ):
                        break
                if starting_custom and not selected:
                    if not flush:
                        return
                    selected = groups
                wait_for_more = (
                    not flush
                    and self.forward_backward_batch is not None
                    and not self.forward_backward_batch.reached(len(data), tokens)
                )
                # Consume empty groups without an RPC; only useful work waits
                # for the submission threshold.
                if wait_for_more and data:
                    return
                groups = selected
                if self.max_staleness > 0:
                    self._accumulating_groups.extend(
                        g.id for g in groups if g.id not in self._accumulating_groups
                    )
                if data:
                    if self._loss_binding.requires_proximal_forward:
                        forward = await self._call(
                            "forward",
                            self.engine.model.forward,
                            await self._model_data(data),
                            **self._policy_guard(),
                            loss_fn="importance_sampling",
                            logprob_temperature=self.engine.temperature,
                        )
                        data, correction, corrected = await call(
                            _decouple,
                            data,
                            forward.logprobs,
                            max_importance_weight=self._loss_binding.max_importance_weight,
                        )
                        self._streamed_corrections.append((corrected, correction))
                if self._streaming_custom_loss is not None:
                    data = await call(
                        custom_batch,
                        data,
                        self._loss_binding.loss,
                        self._loss_binding.input_adapter,
                    )
                await self._submit_backward(data, len(groups))
                if self._streaming_custom_loss is not None:
                    self._streaming_custom_loss.group_order.extend(g.id for g in groups)
                self._streamed_groups.update(g.id for g in groups)
                for group in groups:
                    del self._prepared_groups[self._committed_step, group.id]
                if wait_for_more:
                    return

    async def _prepare_custom_loss(self):
        if (
            self._loss_binding.loss._graph is None
            or self._loss_binding.loss._prepared_for is not self.engine.model
        ):
            self._loss_binding.loss = await call(
                self.engine.model.prepare_loss, self._loss_binding.loss
            )
        if self._overlap:
            self._streaming_custom_loss = StreamingCustomLoss(
                self._loss_binding.loss,
                batch_standardize=self.advantage.standardize == "batch",
                custom_loss_inputs=self._loss_binding.input_adapter,
            )

    def _check_step(self):
        # Model.step currently advances on submission. Only a successfully
        # acknowledged update made by this trainer advances our scheduling head.
        if self.engine.model.step != self._committed_step:
            raise RuntimeError(
                "model step changed outside the trainer; exclusive update ownership is required"
            )

    def _reservation_order(self):
        # Admission is a conservative lower bound on all subsequent segments,
        # including a first sampling request that has not returned yet. Never
        # refresh this bound when a later turn uses newer weights.
        return sorted(self._admitted_policy_steps, key=self._admitted_policy_steps.get)

    def _validate_reservations(self):
        for count, group_id in enumerate(self._reservation_order(), 1):
            deadline = self._admitted_policy_steps[group_id] + self.max_staleness
            capacity = (deadline - self._committed_step + 1) * self.groups_per_step
            if count > capacity:
                raise RuntimeError(
                    "outstanding rollout reservations exceed the staleness window"
                )

    def _min_batch_groups(self):
        floor = self.admission.dynamic_sampling.min_groups_per_step
        return self.groups_per_step if floor is None else floor

    def _sampling_budget_spent(self):
        """Rejections since the previous batch exceed the attempted-group budget.

        Kept and outstanding groups do not spend it, so lookahead and
        oversampling cannot exhaust it without rejections.
        """
        if not self.dynamic_sampling:
            return False
        ratio = self.admission.dynamic_sampling.max_attempted_group_ratio
        return (
            self._dynamic_sampling_counts["rejected"]
            > (ratio - 1) * self.groups_per_step
        )

    def _batch_group_count(self):
        if self._dataset_exhausted or (
            self._sampling_budget_spent() and not self._active
        ):
            # No further candidates can arrive for this batch; train what was kept.
            return min(self.groups_per_step, len(self._pending))
        # The horizon counts batches: a short batch still uses one of `steps`.
        return min(
            self.groups_per_step, self._total_groups - self._n * self.groups_per_step
        )

    def _wait_accumulation_groups(self):
        """Ready groups that can be irrevocably assigned to this update.

        Reserve room for unfinished groups at every deadline, including future
        deadline prefixes that would overflow after an early optimizer step.
        Greedily filling unassigned slots with the oldest reservations proves
        whether a ready candidate can fit without displacing required work.
        """
        ready = {g.id: g for g in self._pending}
        order = self._reservation_order()
        count = self._batch_group_count()
        selected = set(self._accumulating_groups)
        if not selected <= ready.keys() or len(selected) > count:
            raise RuntimeError(
                "accumulation selection is missing ready groups or exceeds the batch"
            )

        def can_finish(chosen):
            planned = set(chosen)
            for group_id in order:
                if len(planned) == count:
                    break
                planned.add(group_id)
            remaining = 0
            for group_id in order:
                if group_id in planned:
                    continue
                remaining += 1
                deadline = self._admitted_policy_steps[group_id] + self.max_staleness
                if remaining > (deadline - self._committed_step) * self.groups_per_step:
                    return False
            return True

        if not can_finish(selected):
            raise RuntimeError("accumulation selection cannot meet rollout deadlines")
        candidates = order[:count] if self.batch_order == "admission" else order
        for group_id in candidates:
            if len(selected) == count:
                break
            if (
                group_id in ready
                and group_id not in selected
                and can_finish(selected | {group_id})
            ):
                selected.add(group_id)
        return [ready[group_id] for group_id in order if group_id in selected]

    def _wait_batch(self):
        if self._overlap and self.max_staleness > 0:
            selected = self._wait_accumulation_groups()
            if len(selected) < self._batch_group_count():
                return None
            selected_ids = {g.id for g in selected}
            return selected, [g for g in self._pending if g.id not in selected_ids]
        ready = {g.id: g for g in self._pending}
        order = self._reservation_order()
        count = self._batch_group_count()
        candidates = (
            order
            if self.batch_order == "admission"
            else [g for g in order if g in ready]
        )
        selected_ids = candidates[:count]
        if len(selected_ids) < count or any(g not in ready for g in selected_ids):
            return None
        selected_set = set(selected_ids)
        # After this update, every deadline prefix must still fit in the
        # remaining training slots. Checking only groups due *now* is too late:
        # several batches can share the same deadline.
        remaining_count = 0
        for group_id in order:
            if group_id in selected_set:
                continue
            remaining_count += 1
            deadline = self._admitted_policy_steps[group_id] + self.max_staleness
            capacity = (deadline - self._committed_step) * self.groups_per_step
            if remaining_count > capacity:
                return None
        return (
            [ready[group_id] for group_id in selected_ids],
            [g for g in self._pending if g.id not in selected_set],
        )

    def _pending_ready(self):
        if self.stale_policy == "wait":
            return self._wait_batch() is not None
        if self.completion.on_stragglers == "carry_over":
            return (
                sum(len(g.trajectories) for g in self._pending)
                >= self.groups_per_step * self.group_size
            )
        return len(self._pending) >= self.groups_per_step

    def _select_batch(self):
        if self.stale_policy == "wait":
            batch = self._wait_batch()
            if batch is None:
                raise RuntimeError("no batch can advance within the staleness window")
            return batch
        if self.completion.on_stragglers != "carry_over":
            return (
                self._pending[: self.groups_per_step],
                self._pending[self.groups_per_step :],
            )
        remaining = self.groups_per_step * self.group_size
        selected, pending = [], []
        for group in self._pending:
            take = min(remaining, len(group.trajectories))
            if take:
                selected.append(
                    dataclasses.replace(group, trajectories=group.trajectories[:take])
                )
                remaining -= take
            if take < len(group.trajectories):
                pending.append(
                    dataclasses.replace(group, trajectories=group.trajectories[take:])
                )
        return selected, pending

    async def _finish_evaluation(self):
        if self._stop.is_set():
            return
        evaluation = asyncio.create_task(self.evaluator.wait())
        stopped = asyncio.create_task(self._stop.wait())
        try:
            done = (
                await asyncio.wait(
                    (evaluation, stopped), return_when=asyncio.FIRST_COMPLETED
                )
            )[0]
            if evaluation in done:
                evaluation.result()
        finally:
            for task in (evaluation, stopped):
                if not task.done():
                    task.cancel()
            await asyncio.gather(evaluation, stopped, return_exceptions=True)

    async def _receive(self):
        result_task = asyncio.create_task(self.engine.next_group())
        stop_task = asyncio.create_task(self._stop.wait())
        try:
            watch = {result_task, stop_task}
            if self._checkpoint_task is not None:
                watch.add(self._checkpoint_task)
            done = (await asyncio.wait(watch, return_when=asyncio.FIRST_COMPLETED))[0]
            if self._checkpoint_task in done:
                self._checkpoint_task.result()
            if result_task not in done:
                return None
            result = result_task.result()
            async with self._lock:
                if self.dynamic_sampling:
                    # Complete groups are accepted/acknowledged atomically. Active
                    # membership deduplicates deliveries without retaining the ids
                    # of every rejected group and trajectory in checkpoints.
                    if result.id not in self._active:
                        self.engine.accept(result)
                        return False
                    unseen = result.trajectories
                else:
                    if result.id in self._finished:
                        self.engine.accept(result)
                        return False
                    unseen = [
                        t for t in result.trajectories if t.id not in self._received
                    ]
                prepared = diagnostics = None
                filtered = False
                if unseen:
                    if self.stale_policy == "wait":
                        admitted = self._admitted_policy_steps[result.id]
                        if any(
                            span.policy_step < admitted
                            for traj in unseen
                            for span in traj.spans
                            if span.kind == "generated"
                        ):
                            raise RuntimeError(
                                "sample policy predates its admission reservation; "
                                "the sampler must follow this trainer's policy updates"
                            )
                    if self.dynamic_sampling:
                        rewards = [
                            value
                            for value in _training_rewards(
                                [unseen],
                                self.truncation,
                                estimator=self.advantage,
                                min_members=self.completion.min_members,
                            )[0]
                            if value is not None
                        ]
                        # Centering equal fractional rewards can leave rounding
                        # residue. Reject exact equality without a tolerance that
                        # would also remove distinct, nearly equal rewards.
                        prepared = (
                            await self._prepare_group(result)
                            if len(rewards) >= max(2, self.completion.min_members)
                            and any(reward != rewards[0] for reward in rewards[1:])
                            else (TrainingBatch(), 0)
                        )
                        keep = self.admission.dynamic_sampling.keep
                        if keep is not None and prepared[0].advantaged():
                            # Before accept: a failing filter keeps the
                            # delivery replayable, like a preparation failure.
                            decision = await call(keep, result)
                            if inspect.isawaitable(decision):
                                decision = await decision
                            if type(decision) is not bool:
                                raise TypeError(
                                    "DynamicSampling.keep must return a bool"
                                )
                            filtered = not decision
                    diagnostics = _rollout_counts(unseen)

                # Validate/prepare before consuming the engine's delivery. A
                # failure leaves it active and in the outbox for checkpoint replay.
                self.engine.accept(result)
                result.trajectories = unseen
                if not self.dynamic_sampling:
                    self._received.update(t.id for t in unseen)
                if result.final:
                    self.engine.acknowledge(result.id)
                    self._active.discard(result.id)
                    if not self.dynamic_sampling:
                        self._finished.add(result.id)
                if unseen:
                    # Match reward/mean's raw environment scores, before
                    # truncation policies and group rejection select training data.
                    scored = [t.reward for t in unseen if not t.dropped]
                    counts = self._dynamic_sampling_counts
                    counts["reward_sum"] = counts.get("reward_sum", 0.0) + sum(scored)
                    counts["reward_count"] = counts.get("reward_count", 0) + len(scored)
                    counts["trajectories"] = counts.get("trajectories", 0) + len(unseen)
                    for key, count in diagnostics.items():
                        counts[key] = counts.get(key, 0) + count
                    if prepared is not None:
                        if filtered or not prepared[0].advantaged():
                            del self._admitted_policy_steps[result.id]
                            counts["rejected"] += 1
                            if filtered:
                                counts["rejected_by_keep"] = (
                                    counts.get("rejected_by_keep", 0) + 1
                                )
                            # Generation spent on groups that never train.
                            counts["rejected_generated_tokens"] = counts.get(
                                "rejected_generated_tokens", 0
                            ) + sum(t.generated_tokens for t in unseen)
                            return True
                        if self._overlap:
                            self._prepared_groups[self._committed_step, result.id] = (
                                prepared
                            )
                    if result.final:
                        self._dynamic_sampling_counts["kept"] += 1
                    if self._spill_directory is not None:
                        # Completed trajectories gain no spans; their arrays
                        # wait on disk until training reads them.
                        if self._scratch is None:
                            self._scratch = await asyncio.to_thread(
                                scratch_spill, self._spill_directory
                            )
                        await asyncio.to_thread(self._scratch.spill, unseen)
                    self._pending.append(result)
                return True
        finally:
            for task in (result_task, stop_task):
                if not task.done():
                    task.cancel()
            await asyncio.gather(result_task, stop_task, return_exceptions=True)

    async def _admit_available(self, rows):
        self._dataset_exhausted = (
            not self.repeat_dataset
            and self._submitted >= len(rows)
            and not self._active
        )
        if not self.repeat_dataset and self._submitted >= len(rows):
            return
        if self._sampling_budget_spent():
            # Stop refilling. Groups already sampling may still fill the batch;
            # fail once they can no longer reach the minimum batch.
            if len(self._admitted_policy_steps) < self._min_batch_groups():
                ratio = self.admission.dynamic_sampling.max_attempted_group_ratio
                raise SamplingExhausted(
                    batch=self._n + 1,
                    rejected=self._dynamic_sampling_counts["rejected"],
                    limit=f"max_attempted_group_ratio ({ratio})",
                )
            return
        ahead = self.admission.batches_ahead
        desired = min(
            (1 + self.max_staleness) * self.groups_per_step,
            math.ceil((1 + ahead) * self.groups_per_step * self.admission.oversample),
        )
        if self.dynamic_sampling:
            # Attempts have unique ids and advance the dataset cursor, but only
            # retained groups spend the training horizon. Every outstanding
            # candidate still reserves a slot until it is rejected or trained.
            remaining = self._total_groups - self._n * self.groups_per_step
            limit = (
                self._submitted
                + min(desired, remaining)
                - len(self._admitted_policy_steps)
            )
            if not self.repeat_dataset:
                limit = min(limit, len(rows))
        else:
            limit = min(self._total_groups, self._n * self.groups_per_step + desired)
        if self._submitted < limit:
            await self._publish_sampling_snapshot()
        while self._submitted < limit:
            row = (
                rows[self._submitted % len(rows)]
                if self.dataset_scheduler is None
                else self.dataset_scheduler.row(self._submitted, rows)
            )
            self._admit(row, f"group-{self._submitted}")
            self._submitted += 1

    async def run(self, dataset, *, steps: int, after_recovery=None):
        """Yield a :class:`Step` after each completed training batch.

        Args:
            dataset: Rows used to create rollout groups.
            steps: Maximum batches with dynamic sampling on a finite dataset;
                otherwise the number of batches to complete (raises if more than
                a finite dataset can supply without filtering). A finite dataset
                ends with a smaller batch if informative groups remain. Without
                filtering, an unusable batch counts but does not update the model.
                The learning-rate schedule still uses this requested horizon;
                early dataset exhaustion does not rescale it. Use repeat_dataset=True
                to target the full horizon (subject to the sampling budget).
            after_recovery: Optional async callback receiving the number of
                restored batches before new training starts. It also runs if
                all requested batches were already complete. Make it
                idempotent, because recovery may retry it.
        """
        if self._running:
            raise RuntimeError("trainer is already running")
        _integer(steps, "steps", 1)
        self._full_weight = getattr(self.engine.model, "full_weight", False) is True
        rows = list(dataset)
        image_session = self._image_session()
        if not rows or steps < 1:
            raise ValueError("run requires a nonempty dataset and positive steps")
        if self.evaluator is not None:
            rows = self.evaluator.exclude_holdout(rows)
            if not rows:
                raise ValueError("no training rows remain after holdout exclusion")
        available_batches = math.ceil(len(rows) / self.groups_per_step)
        if (
            not self.repeat_dataset
            and not self.dynamic_sampling
            and steps > available_batches
        ):
            raise ValueError(
                "steps exceeds the finite dataset; enable repeat_dataset to cycle"
            )
        if self._loss_binding.is_custom:
            self._running = True
            try:
                preparation = asyncio.create_task(self._prepare_custom_loss())
                try:
                    await asyncio.shield(preparation)
                except asyncio.CancelledError:
                    drain = asyncio.gather(preparation, return_exceptions=True)
                    while not drain.done():
                        try:
                            await asyncio.shield(drain)
                        except asyncio.CancelledError:
                            pass
                    raise
            finally:
                self._running = False
        self._total_groups = steps * self.groups_per_step
        if not self.repeat_dataset:
            self._total_groups = min(self._total_groups, len(rows))
        self._n, self._submitted = 0, 0
        self._dataset_exhausted = False
        self._dynamic_sampling_counts = {"kept": 0, "rejected": 0}
        self._active, self._finished, self._received = set(), set(), set()
        self._pending, self._journal = [], []
        self._updates_since_save = 0
        self._prepared_groups.clear()
        self._durable_base = False
        self._accumulating_groups = []
        self._admitted_policy_steps = {}
        self._base = None
        self._stop, self._lock = asyncio.Event(), asyncio.Lock()
        self._state_write = None
        self._saved_model_step = None
        self._last_state_save = time.monotonic()
        self._checkpoint_task = None
        self._pending_backwards = []
        self._backward_group_batches = []
        self._streamed_chunks, self._streamed_results = [], []
        self._committed_step = None
        self._backward_executor = None
        self._updating = False
        self._fingerprints = {
            "row_order_fingerprint": row_order_fingerprint(rows),
            "plan_fingerprint": training_plan_fingerprint(
                rows, self.groups_per_step, steps, repeat_dataset=self.repeat_dataset
            ),
            "steps": steps,
        }
        if self.checkpoint:
            config = self._config()
            self._fingerprints["config_fingerprint"] = fingerprint(config)
            compatible_fingerprints = self._compatible_config_fingerprints(config)
        self._run_key = self._fingerprints["plan_fingerprint"][:12]
        store_context = (
            StateStore(self.checkpoint, spill_arrays=self._spill_arrays)
            if self.checkpoint
            else nullcontext()
        )
        handlers = {}
        healthy = True
        recovered = 0
        self._activities = Activities()
        self._published_sampling_step = None
        self._running = True
        self._status = "running"
        previous_snapshot_sampling = self.engine._latest_snapshot_sampling
        metrics_task = None
        try:
            reporter = MetricsReporter(
                self.engine.model,
                steps=self.metrics.steps,
                interval=self.metrics.interval,
            )
            if reporter.enabled and self.metrics.interval is not None:
                metrics_task = asyncio.create_task(reporter._report_progress(self))
            # Only the trainer publishes snapshots before each admission.
            # Standalone trajectory rollouts must still select current weights.
            self.engine._latest_snapshot_sampling = (
                callable(getattr(self.engine.model, "submit_sampling_batch", None))
                and getattr(self.engine.model, "checkpoint", None) is None
            )
            with store_context as self._store:
                saved = (
                    self._store.load(lazy_records=True, restore=True)
                    if self._store
                    else None
                )
                resumed = bool(saved)
                if saved:
                    self._durable_base = saved.get("durable_base", False)
                    self._updates_since_save = saved.get(
                        "updates_since_save", len(saved["journal"])
                    )
                    if self.init_checkpoint is not None:
                        raise ValueError(
                            "init_checkpoint is mutually exclusive with automatic resume"
                        )
                    if self._uses_admission:
                        saved_schedule = saved.get("sampling_schedule", {})
                        saved_ahead = saved_schedule.get("admit_ahead")
                        if (
                            type(saved_ahead) is int
                            and saved_ahead >= 0
                            and min(saved_ahead, self.max_staleness)
                            == self.admission.batches_ahead
                        ):
                            # Preserve the old spelling of an equivalent clamped
                            # window, including in subsequent saves for rollback.
                            self._fingerprint_ahead = saved_ahead
                        saved_oversample = saved_schedule.get("oversample_factor")
                        if (
                            type(saved_oversample) in (int, float)
                            and saved_oversample == self.admission.oversample
                        ):
                            # JSON distinguishes legacy integer and float spellings.
                            self._fingerprint_oversample = saved_oversample
                        config = config | {
                            "schedule": config["schedule"]
                            | {
                                "admit_ahead": self._fingerprint_ahead,
                                "oversample_factor": self._fingerprint_oversample,
                            }
                        }
                        self._fingerprints["config_fingerprint"] = fingerprint(config)
                        compatible_fingerprints = self._compatible_config_fingerprints(
                            config
                        )
                    if saved.get("version") != 1 or any(
                        saved.get(k) != v
                        and (
                            k != "config_fingerprint"
                            or saved.get(k) not in compatible_fingerprints
                        )
                        for k, v in self._fingerprints.items()
                    ):
                        raise ValueError(
                            "resume dataset, order, holdout, schedule, or training configuration changed"
                        )
                if self._store and image_session is not None:
                    restored = await self._call(
                        "restore_images",
                        image_session.restore_images,
                        {"rows": rows, "saved": saved},
                        image_store=self._store.images,
                    )
                    rows, saved = restored["rows"], restored["saved"]
                    del restored
                from river_client.images import image_handles, map_images

                self._dataset_images = list(
                    {image.sha256: image for image in image_handles(rows)}.values()
                )
                # Handles already uploaded to this session, by content, so
                # lazily replayed journal records do not upload them again.
                session_images = (
                    {}
                    if image_session is None
                    else {
                        image.sha256: image
                        for image in image_handles((rows, saved))
                        if image.session_id == image_session.session_id
                    }
                )
                async with self.engine:
                    reporter.include_rollouts = True
                    sampling_before = self.engine.sampling_metrics()
                    if self._full_weight and self.engine.server_capabilities:
                        self.engine.server_capabilities.require_model(
                            self.engine.model.base_model, "full_weight_rl_v1"
                        )
                        if self.evaluator is not None:
                            self.engine.server_capabilities.require_model(
                                self.engine.model.base_model,
                                "full_weight_checkpoint_sampling_v1",
                            )
                    await self._refresh_policy()
                    readmit = None
                    checkpoint_recovery = False
                    if saved and self._full_weight:
                        readmit, checkpoint_recovery = await self._resume_full_weight(
                            saved
                        )
                    elif saved:
                        self._base = Checkpoint(**saved["base"])
                        await self._call(
                            "load_weights",
                            self.engine.model.load_weights,
                            self._base,
                            load_optimizer=True,
                        )
                        await self._refresh_policy()
                        # Replay the committed updates after the last expensive
                        # weights checkpoint before restoring newer rollout state.
                        # This preserves policy-step provenance after a rewind.
                        self._journal = saved["journal"]
                        for record in self._journal:
                            # Records load one at a time, not as a whole journal.
                            update = await asyncio.to_thread(self._store.read, record)
                            if image_session is not None and update is not record:
                                update = await self._call(
                                    "restore_images",
                                    image_session.restore_images,
                                    map_images(
                                        update,
                                        lambda image: session_images.get(
                                            image.sha256, image
                                        ),
                                    ),
                                    image_store=self._store.images,
                                )
                                session_images.update(
                                    (image.sha256, image)
                                    for image in image_handles(update)
                                )
                            update = self._restore_update(update)
                            await self._update(
                                update.get("data"),
                                update["optimizer"],
                                chunks=update.get("chunks"),
                                recovering=True,
                            )
                            recovered += 1
                        if self.engine.model.step != saved["model_step"]:
                            raise ValueError(
                                "recovered optimizer step disagrees with saved trainer state"
                            )
                    if saved:
                        self._n, self._submitted = saved["n"], saved["submitted"]
                        self._dynamic_sampling_counts = dict(
                            saved.get(
                                "dynamic_sampling_counts", {"kept": 0, "rejected": 0}
                            )
                        )
                        self._active, self._finished, self._received = (
                            set(saved["active"]),
                            set(saved["finished"]),
                            set(saved["received"]),
                        )
                        restored_trajectories = {}
                        self._pending = [
                            group_from_state(g, restored_trajectories)
                            for g in saved["pending"]
                        ]
                        if self._overlap and self.max_staleness > 0:
                            self._accumulating_groups = saved["accumulating_groups"]
                        self._admitted_policy_steps = dict(
                            saved.get("admitted_policy_steps", {})
                        )
                        if self.stale_policy == "wait" and set(
                            self._admitted_policy_steps
                        ) != (self._active | {g.id for g in self._pending}):
                            raise ValueError(
                                "resume is missing outstanding rollout reservations"
                            )
                        # Restoring the engine starts continuation tasks. Publish
                        # before those tasks can select a pre-recovery snapshot;
                        # retain the existing on-disk engine state if export fails.
                        await self._publish_sampling_snapshot(recovering=True)
                        if self.dataset_scheduler is not None:
                            self.dataset_scheduler.load_state_dict(
                                saved["dataset_scheduler"]
                            )
                        self.engine.load_state_dict(
                            saved["engine"],
                            restart_pinned_trajectories=self.engine._latest_snapshot_sampling,
                            trajectories=restored_trajectories,
                        )
                        del restored_trajectories
                        if self.evaluator:
                            self.evaluator.load_state_dict(
                                saved["eval_history"], model=self.engine.model
                            )
                        if readmit is not None:
                            for group_id, row in readmit:
                                self._admit(row, group_id)
                            if checkpoint_recovery:
                                await self._save_weights()
                            else:
                                await self._save_state()
                    else:
                        if self.init_checkpoint is not None:
                            # A full-weight run loads only with its optimizer
                            # state; the server refuses a weights-only load.
                            await call(
                                self.engine.model.load_weights,
                                self.init_checkpoint,
                                load_optimizer=self._full_weight,
                            )
                            await self._refresh_policy()
                        if self._store and self._full_weight:
                            await self._save_state()
                        elif self._store:
                            await self._save_weights()
                    # Restored objects now own their data; release the decoded
                    # checkpoint rather than keeping it for the whole run.
                    saved = None
                    self._committed_step = self.engine.model.step
                    # Reconcile external effects of the last committed batch
                    # before another update, including a fully completed run.
                    if resumed and after_recovery is not None:
                        await after_recovery(self._n)
                    self._validate_reservations()
                    if self.evaluator:
                        await self.evaluator.launch(
                            self.engine.model,
                            self._n,
                            **(
                                {"on_checkpoint": self._save_state}
                                if self._store and self._full_weight
                                else {}
                            ),
                        )
                    for name in self.checkpoint.on_signal if self.checkpoint else ():
                        sig = getattr(signal, name)
                        handlers[sig] = signal.getsignal(sig)
                        asyncio.get_running_loop().add_signal_handler(
                            sig, self._stop.set
                        )
                    if self._store:
                        self._checkpoint_task = asyncio.create_task(
                            self._periodic_checkpoint()
                        )
                    try:
                        while self._n < steps and not self._stop.is_set():
                            self._backward_group_batches = []
                            (
                                self._streamed_groups,
                                self._streamed_chunks,
                                self._streamed_results,
                            ) = (
                                set(),
                                [],
                                [],
                            )
                            self._streamed_corrections = []
                            if self._streaming_custom_loss is not None:
                                self._streaming_custom_loss.group_order = []
                            batch_started = time.monotonic()
                            batch_operations = self._activities.snapshot()
                            if (
                                self._checkpoint_task is not None
                                and self._checkpoint_task.done()
                            ):
                                self._checkpoint_task.result()
                            self._check_step()
                            self._validate_reservations()
                            async with self._lock:
                                await self._admit_available(rows)
                            wait_seconds, wait_count = 0.0, 0
                            # Restored pending groups may already have populated
                            # worker gradients in the old process. Rebuild them.
                            await self._accumulate_ready()
                            while not self._pending_ready() and not self._stop.is_set():
                                if not self._active:
                                    break
                                blocked = (
                                    self.stale_policy == "wait"
                                    and len(self._pending) >= self.groups_per_step
                                )
                                wait_started = time.monotonic()
                                await self._receive()
                                if self.dynamic_sampling and not self._stop.is_set():
                                    async with self._lock:
                                        await self._admit_available(rows)
                                await self._accumulate_ready()
                                if blocked:
                                    wait_seconds += time.monotonic() - wait_started
                                    wait_count += 1
                                self._check_step()
                            if self._stop.is_set():
                                break
                            if not self._pending:
                                if self._admitted_policy_steps:
                                    raise RuntimeError(
                                        "rollout engine ended with unconsumed reservations"
                                    )
                                break
                            await self._accumulate_ready(flush=True)
                            await self._collect_backwards(all_pending=True)
                            if self._stop.is_set():
                                break
                            async with self._lock:
                                self._check_step()
                                selected, remaining_pending = self._select_batch()
                                backward_groups = selected
                                if self._streaming_custom_loss is not None:
                                    positions = {
                                        key: i
                                        for i, key in enumerate(
                                            self._streaming_custom_loss.group_order
                                        )
                                    }
                                    backward_groups = sorted(
                                        selected, key=lambda g: positions[g.id]
                                    )
                                started = (
                                    batch_started if self._overlap else time.monotonic()
                                )
                                operation_before = (
                                    batch_operations
                                    if self._overlap
                                    else self._activities.snapshot()
                                )
                                trajectories = [
                                    t for g in selected for t in g.trajectories
                                ]
                                self._apply_policy_provenance(trajectories)
                                data, metrics = await call(
                                    _build_batch,
                                    [g.trajectories for g in backward_groups],
                                    estimator=self.advantage,
                                    normalize=self._loss_binding.normalize,
                                    truncation=self.truncation,
                                    min_members=self.completion.min_members,
                                    current_step=self.engine.model.step,
                                    max_staleness=(
                                        self.max_staleness
                                        if self.stale_policy == "mask_span"
                                        else None
                                    ),
                                    include_loss_mask=self._loss_binding.is_custom,
                                    loss=self._loss_binding,
                                )
                                if self._loss_binding.is_custom:
                                    if (
                                        not self._loss_binding.train_zero_advantage_batches
                                        and not data.advantaged()
                                    ):
                                        data = TrainingBatch()
                                    if self._streaming_custom_loss is None:
                                        data = await call(
                                            custom_batch,
                                            data,
                                            self._loss_binding.loss,
                                            self._loss_binding.input_adapter,
                                        )
                                    metrics["train/datums"] = float(len(data))
                                if self.validate_batch is not None:
                                    await call(
                                        self.validate_batch, trajectories, metrics
                                    )
                                if data:
                                    if (
                                        self._loss_binding.requires_proximal_forward
                                        and not self._overlap
                                    ):
                                        forward = await self._call(
                                            "forward",
                                            self.engine.model.forward,
                                            await self._model_data(data),
                                            **self._policy_guard(),
                                            loss_fn="importance_sampling",
                                            logprob_temperature=self.engine.temperature,
                                        )
                                        data, correction_metrics, _ = await call(
                                            _decouple,
                                            data,
                                            forward.logprobs,
                                            max_importance_weight=self._loss_binding.max_importance_weight,
                                        )
                                        metrics.update(correction_metrics)
                                    optimizer_kwargs = self.optimizer.kwargs(
                                        self._n, steps
                                    )
                                    self._check_step()
                                    self._updating = True
                                    if not self._overlap:
                                        fb, optim = await self._update(
                                            data, optimizer_kwargs
                                        )
                                        update = {
                                            "data": data,
                                            "optimizer": optimizer_kwargs,
                                        }
                                    else:
                                        if (
                                            {g.id for g in selected}
                                            != self._streamed_groups
                                            or not self._streamed_chunks
                                        ):
                                            raise RuntimeError(
                                                "optimizer cannot commit an incomplete backward batch"
                                            )
                                        fb = _merge_forward_backward_sub_batch_results(
                                            self._streamed_results,
                                            [len(c) for c in self._streamed_chunks],
                                            custom=self._loss_binding.is_custom,
                                        )
                                        scale = accumulation_scale(
                                            [g.trajectories for g in selected],
                                            estimator=self.advantage,
                                            truncation=self.truncation,
                                            min_members=self.completion.min_members,
                                            normalize=self._loss_binding.normalize,
                                            metrics=metrics,
                                        )
                                        if self._streaming_custom_loss is not None:
                                            loss_metrics, scale = await call(
                                                self._streaming_custom_loss.finish,
                                                data,
                                                self._streamed_chunks,
                                                self._streamed_results,
                                                scale,
                                            )
                                            fb = dataclasses.replace(
                                                fb, metrics=fb.metrics | loss_metrics
                                            )
                                        if scale != 1.0:
                                            optimizer_kwargs["gradient_scale"] = scale
                                            if (
                                                self._streaming_custom_loss is None
                                                and "loss" in fb.metrics
                                            ):
                                                fb.metrics["loss"] *= scale
                                        if self._streamed_corrections:
                                            count = sum(
                                                n
                                                for n, correction in self._streamed_corrections
                                            )
                                            for key in self._streamed_corrections[0][1]:
                                                metrics[key] = sum(
                                                    n * correction[key]
                                                    for n, correction in self._streamed_corrections
                                                ) / max(1, count)
                                        metrics["train/gradient_scale"] = scale
                                        optim = await self._optimize(optimizer_kwargs)
                                        # Keep chunk boundaries and completion order
                                        # when replaying committed steps after a restore.
                                        update = {
                                            "chunks": self._streamed_chunks,
                                            "optimizer": optimizer_kwargs,
                                        }
                                    # A full-weight resume never replays updates
                                    # (R56), so it keeps no journal.
                                    if self._store:
                                        self._updates_since_save += 1
                                        if not self._full_weight:
                                            self._journal.append(update)
                                    self._committed_step = self.engine.model.step
                                    self._updating = False
                                    metrics.update(
                                        {f"loss/{k}": v for k, v in fb.metrics.items()}
                                    )
                                    metrics.update(
                                        {
                                            f"optimizer/{k}": v
                                            for k, v in optim.metrics.items()
                                        }
                                    )
                                self._pending = remaining_pending
                                self._accumulating_groups = []
                                self._prepared_groups.clear()
                                if self.stale_policy == "wait":
                                    for group in selected:
                                        del self._admitted_policy_steps[group.id]
                                    self._validate_reservations()
                                self._n += 1
                                counts = self._dynamic_sampling_counts
                                if self.dynamic_sampling:
                                    kept = counts["kept"]
                                    rejected = counts["rejected"]
                                    metrics.update(
                                        {
                                            "sampling/groups_kept": float(kept),
                                            "sampling/groups_rejected": float(rejected),
                                            "sampling/rejected_generated_tokens": float(
                                                counts.get(
                                                    "rejected_generated_tokens", 0
                                                )
                                            ),
                                            "train/groups": float(len(selected)),
                                        }
                                    )
                                    if self.admission.dynamic_sampling.keep is not None:
                                        metrics["sampling/groups_rejected_by_keep"] = (
                                            float(counts.get("rejected_by_keep", 0))
                                        )
                                    if kept + rejected:
                                        metrics["sampling/group_acceptance_rate"] = (
                                            kept / (kept + rejected)
                                        )
                                scored = counts.get("reward_count", 0)
                                if scored:
                                    metrics["sampling/reward_mean"] = (
                                        counts["reward_sum"] / scored
                                    )
                                for key, count in counts.items():
                                    if key.startswith("rollout/"):
                                        metrics[f"sampling/{key}"] = float(count)
                                    elif key.startswith("truncated/"):
                                        metrics[f"sampling/{key}"] = (
                                            count / counts["trajectories"]
                                        )
                                self._dynamic_sampling_counts = {
                                    "kept": 0,
                                    "rejected": 0,
                                }
                                if self.dataset_scheduler is not None:
                                    metrics.update(
                                        self.dataset_scheduler.commit(self._n, selected)
                                    )
                                metrics.update(
                                    {
                                        "staleness/wait_seconds": wait_seconds,
                                        "staleness/wait_count": float(wait_count),
                                        "staleness/reserved_groups": float(
                                            len(self._admitted_policy_steps)
                                        ),
                                        "train/updated": float(bool(data)),
                                        "train/backward_chunks": (
                                            float(len(self._streamed_chunks))
                                            if self._overlap
                                            else float(bool(data))
                                        ),
                                        "train/batch_seconds": time.monotonic()
                                        - batch_started,
                                        "train/seconds": time.monotonic() - started,
                                        "groups/deadline_frac": sum(
                                            g.closed_by_deadline for g in selected
                                        )
                                        / len(selected),
                                        "groups/mean_wait_seconds": sum(
                                            g.wait_seconds for g in selected
                                        )
                                        / len(selected),
                                        "throughput/queue_depth": float(
                                            self.engine._ready.qsize()
                                        ),
                                        "recovery/steps_replayed": float(recovered),
                                        **{
                                            f"recovery/{k}": float(v)
                                            for k, v in self.engine.recovery_metrics.items()
                                        },
                                    }
                                )
                                sampling = self.engine.sampling_metrics()
                                metrics.update(
                                    _sampling_interval(sampling, sampling_before)
                                )
                                sampling_before = sampling
                                for operation in ("forward", "backward", "optimizer"):
                                    total = (
                                        self._activities.snapshot()
                                        .get(operation, {})
                                        .get("seconds", 0.0)
                                    )
                                    previous = operation_before.get(operation, {}).get(
                                        "seconds", 0.0
                                    )
                                    metrics[f"train/{operation}_seconds"] = (
                                        total - previous
                                    )
                                if (
                                    self._store
                                    and self._updates_since_save
                                    >= self.checkpoint.weights_every
                                ):
                                    await self._save_weights(
                                        durable=self._n == steps
                                        or (
                                            self._dataset_exhausted
                                            and not self._pending
                                        )
                                    )
                                if self.evaluator:
                                    try:
                                        await self.evaluator.launch(
                                            self.engine.model,
                                            self._n,
                                            final=self._n == steps
                                            or (
                                                self._dataset_exhausted
                                                and not self._pending
                                            ),
                                            **(
                                                {"on_checkpoint": self._save_state}
                                                if self._store and self._full_weight
                                                else {}
                                            ),
                                        )
                                    except Exception:
                                        # Evaluation cannot roll back an optimizer
                                        # update that has already completed.
                                        if self._store:
                                            await self._save_state()
                                        raise
                                step = Step(
                                    self._n,
                                    self.engine.model.step,
                                    metrics,
                                    trajectories,
                                )
                            reporter.log_step(step)
                            yield step
                        if (
                            self.dynamic_sampling
                            and self._dataset_exhausted
                            and self._n == 0
                            and not self._stop.is_set()
                        ):
                            warnings.warn(
                                "dynamic_sampling exhausted the finite dataset without "
                                "a trainable group; no training updates were performed",
                                RuntimeWarning,
                                stacklevel=2,
                            )
                        if self.evaluator:
                            try:
                                if (
                                    self._dataset_exhausted
                                    and self._n > 0
                                    and not self._pending
                                    and not self._stop.is_set()
                                ):
                                    async with self._lock:
                                        await self.evaluator.launch(
                                            self.engine.model,
                                            self._n,
                                            final=True,
                                            **(
                                                {"on_checkpoint": self._save_state}
                                                if self._store and self._full_weight
                                                else {}
                                            ),
                                        )
                                await self._finish_evaluation()
                            except Exception:
                                # Background rollout/logging failures do not
                                # invalidate already committed training updates.
                                if self._store:
                                    async with self._lock:
                                        await self._save_state()
                                raise
                    except SamplingExhausted:
                        # No optimizer was submitted. The normal finalizer drains
                        # partial backward work and saves pending groups/counters;
                        # recovery rebuilds gradients from those retained groups.
                        raise
                    except Exception as error:
                        healthy = False
                        # Stop periodic writes before the rewind RPC can yield
                        # with a failed optimizer's state still in memory.
                        if self._checkpoint_task:
                            self._checkpoint_task.cancel()
                        if self._full_weight:
                            await self._raise_if_rewound(error)
                        raise
                    finally:
                        # A failed receive/update may leave transient state that
                        # must not replace the last recoverable checkpoint while
                        # outstanding backward calls are being drained.
                        if self._checkpoint_task:
                            self._checkpoint_task.cancel()
                        # Submitted RPCs keep running even if their waiter is
                        # cancelled. Drain before closing/checkpointing a model;
                        # failed contributions must never reach an optimizer.
                        checkpoint_failure = None
                        try:
                            failure = await self._drain_backwards()
                            backward_failure = failure if healthy else None
                            if failure is not None:
                                healthy = False
                        finally:
                            # The drain can re-raise cancellation. Keep the
                            # directory lock until its writer also finishes.
                            if self._checkpoint_task:
                                result = await asyncio.gather(
                                    self._checkpoint_task, return_exceptions=True
                                )
                                if isinstance(result[0], Exception):
                                    healthy = False
                                    checkpoint_failure = result[0]
                        # Preserve cancellation from the backward drain once
                        # the writer has finished, even if that write failed.
                        if checkpoint_failure is not None:
                            raise checkpoint_failure
                        if self._store and healthy and not self._updating:
                            async with self._lock:
                                if (
                                    self._n == steps
                                    or (self._dataset_exhausted and not self._pending)
                                ) and (
                                    self._updates_since_save or not self._durable_base
                                ):
                                    await self._save_weights(durable=True)
                                else:
                                    await self._save_state()
                        if backward_failure is not None:
                            raise backward_failure
        except BaseException as error:
            self._status = (
                "stopped"
                if isinstance(error, (asyncio.CancelledError, GeneratorExit))
                else "failed"
            )
            raise
        finally:
            if metrics_task is not None:
                metrics_task.cancel()
            try:
                # Recovery and checkpoint writes can fail before the training
                # loop's cleanup. Always cancel background evaluation tasks.
                if self.evaluator:
                    await self.evaluator.close()
            except BaseException:
                self._status = "failed"
                raise
            finally:
                self._prepared_groups.clear()
                self.engine._latest_snapshot_sampling = previous_snapshot_sampling
                if self._status == "running":
                    self._status = (
                        "completed"
                        if self._n == steps
                        or (
                            self._dataset_exhausted
                            and not self._pending
                            and not self._stop.is_set()
                        )
                        else "stopped"
                    )
                for sig, handler in handlers.items():
                    asyncio.get_running_loop().remove_signal_handler(sig)
                    signal.signal(sig, handler)
                try:
                    if metrics_task is not None:
                        await asyncio.gather(metrics_task, return_exceptions=True)
                        reporter.log_progress(self)
                finally:
                    self._running = False


def run(trainer: AsyncTrainer, dataset, *, steps: int, on_step=None):
    """Run training from synchronous Python code and return the final step.

    Args:
        trainer: Configured trainer to run.
        dataset: Rows used to create rollout groups.
        steps: Number of training batches to complete.
        on_step: Optional callback called with each completed ``Step``.

    In an async program, iterate over ``trainer.run(...)`` instead.
    """

    async def consume():
        last = None
        async for last in trainer.run(dataset, steps=steps):
            if on_step is not None:
                await call(on_step, last)
        return last

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(consume())
    raise RuntimeError(
        "rl.run cannot nest an event loop; use 'async for step in trainer.run(...)'"
    )


def _recovered(data):
    """Mark journal data as restored, which allows routing fallback."""
    if isinstance(data, TrainingBatch):
        return data.with_items(recovered=True, drop_recovery=False)
    return [dict(d, _rl_recovered_routing=True) for d in data]


def _routing(data):
    """Per datum: (has a routing capture, restored from a checkpoint)."""
    if isinstance(data, TrainingBatch):
        return data.routing()
    return [
        (bool(d.get("expert_routing_handle")), bool(d.get("_rl_recovered_routing")))
        for d in data
    ]
