"""Async RL composition over Model.forward[_backward] and Model.optim_step."""

from __future__ import annotations

import asyncio
import copy
import dataclasses
import inspect
import math
import signal
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import nullcontext
from dataclasses import dataclass
from typing import Literal

from river_client.client import (
    _ForwardBackwardNeedsSubBatches,
    _merge_forward_backward_sub_batch_results,
)
from river_client.types import Checkpoint

from .advantages import (
    Batchwise,
    GroupCentered,
    accumulation_scale,
    build_batch,
    decouple_ppo,
    reward_values,
)
from .checkpoint import (
    Checkpointing,
    StateStore,
    fingerprint,
    row_order_fingerprint,
    training_plan_fingerprint,
)
from .config import (
    Adam,
    ForwardBackwardBatch,
    GroupCompletion,
    Truncation,
    _integer,
    acknowledge_risk,
)
from .engine import call, group_from_state, group_state
from .env import Env
from .progress import Activities
from .trajectory import Span


@dataclass
class Step:
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


_DEFAULT_TRUNCATION = Truncation()


class AsyncTrainer:
    """Consume completion batches while new rollouts continue on shared capacity.

    ``steps`` counts consumed batches, including reported zero-gradient skips.
    ``Step.model_step`` counts actual optimizer updates. With max_staleness=0,
    admission is restricted to the current batch, giving synchronous semantics.
    The default ``stale_policy="wait"`` retains whole oversampled groups and
    reserves training capacity through their admission step + max_staleness.
    This trainer must be the model's only update writer.
    """

    def __init__(
        self,
        *,
        engine,
        optimizer: Adam,
        completion: GroupCompletion,
        normalize: str,
        groups_per_step: int,
        group_size: int = 16,
        advantage=None,
        loss: str = "cispo",
        max_staleness: int = 2,
        stale_policy: str = "wait",
        allow_trajectory_loss: bool = False,
        allow_unbounded_staleness: bool = False,
        truncation: Truncation = _DEFAULT_TRUNCATION,
        checkpoint: Checkpointing | None = None,
        init_checkpoint=None,
        evaluator=None,
        run_config=None,
        max_importance_weight: float = 5.0,
        routing_replay: bool = False,
        repeat_dataset: bool = True,
        batch_order: str = "completion",
        validate_batch=None,
        forward_backward_groups: int | None = None,
        forward_backward_batch: ForwardBackwardBatch | Literal["auto"] | None = "auto",
        max_pending_forward_backward: int = 16,
        **loss_config,
    ):
        if engine.temperature <= 0 or not math.isfinite(engine.temperature):
            raise ValueError(
                "RL training requires a finite positive sampling temperature"
            )
        _integer(max_pending_forward_backward, "max_pending_forward_backward", 1)
        self.max_pending_forward_backward = max_pending_forward_backward
        _integer(groups_per_step, "groups_per_step", 1)
        _integer(group_size, "group_size", 1)
        _integer(max_staleness, "max_staleness")
        if normalize not in {"token", "sequence", "batch", "sum"}:
            raise ValueError(
                "normalize must be explicitly token, sequence, batch, or sum"
            )
        if (
            groups_per_step < 1
            or group_size < completion.min_members
            or max_staleness < 0
        ):
            raise ValueError("invalid batch size, group quorum, or staleness limit")
        if loss not in {"cispo", "ppo", "importance_sampling", "decoupled_ppo"}:
            raise ValueError("unsupported RL loss")
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
        if routing_replay and loss == "decoupled_ppo":
            raise ValueError(
                "decoupled_ppo forward does not support forced routing replay"
            )
        self.routing_replay, self.repeat_dataset, self.batch_order = (
            routing_replay,
            repeat_dataset,
            batch_order,
        )
        self.advantage = advantage if advantage is not None else GroupCentered()
        # These unreleased names were renamed; **loss_config must not silently
        # send a misspelled scheduling option to the loss function.
        for old_name, new_name in (
            ("backward_groups", "forward_backward_groups"),
            ("backward_batch", "forward_backward_batch"),
            ("max_pending_backward", "max_pending_forward_backward"),
        ):
            if old_name in loss_config:
                raise TypeError(f"{old_name} was renamed to {new_name}")
        if forward_backward_batch == "auto":
            eligible = (
                max_staleness == 0
                and stale_policy == "wait"
                and completion.mode == "wait"
                and engine.sampling_policy == "trajectory"
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
        if forward_backward_groups is not None:
            _integer(forward_backward_groups, "forward_backward_groups", 1)
            if forward_backward_groups > groups_per_step:
                raise ValueError(
                    "forward_backward_groups cannot exceed groups_per_step"
                )
        if self._overlap:
            if (
                max_staleness != 0
                or stale_policy != "wait"
                or completion.mode != "wait"
            ):
                raise ValueError(
                    "streaming backward requires synchronous max_staleness=0 and wait completion/staleness"
                )
            if engine.sampling_policy != "trajectory":
                raise ValueError(
                    "streaming backward requires trajectory-pinned sampling"
                )
            if type(self.advantage) is not GroupCentered:
                raise ValueError(
                    "streaming backward currently requires GroupCentered advantages"
                )
        self.forward_backward_groups = forward_backward_groups
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
            completion.on_stragglers == "carry_over"
            or engine.schedule.oversample_factor != 1
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
        allowed = {
            "cispo": {"eps_max"},
            "ppo": {"clip_low", "clip_high"},
            "decoupled_ppo": {"clip_low", "clip_high"},
            "importance_sampling": set(),
        }[loss]
        if set(loss_config) - allowed:
            raise ValueError(
                f"unsupported {loss} options: {sorted(set(loss_config) - allowed)}"
            )
        self.engine, self.optimizer, self.completion = engine, optimizer, completion
        self.normalize, self.groups_per_step, self.group_size = (
            normalize,
            groups_per_step,
            group_size,
        )
        self.loss, self.loss_config = (
            loss,
            {"logprob_temperature": engine.temperature, **loss_config},
        )
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
        self.run_config = copy.deepcopy(run_config or {})
        if not math.isfinite(max_importance_weight) or max_importance_weight <= 0:
            raise ValueError("max_importance_weight must be finite and positive")
        if any(not math.isfinite(v) or v < 0 for v in loss_config.values()):
            raise ValueError("loss configuration values must be finite and nonnegative")
        if validate_batch is not None and not callable(validate_batch):
            raise TypeError("validate_batch must be callable")
        self.validate_batch = validate_batch
        self.max_importance_weight = max_importance_weight
        self._running = False
        self._status = "idle"
        self._activities = Activities()

    def progress(self):
        """Snapshot client progress, safe before, during, and after a run.

        `model_step` is the last acknowledged update, not Model.step's
        submission-time counter. No server queue/allocation details are read.
        """
        return {
            "status": self._status,
            "batches": getattr(self, "_n", 0),
            "backward_groups_completed": len(getattr(self, "_streamed_groups", ()))
            - sum(
                count for index, task, count in getattr(self, "_pending_backwards", ())
            ),
            "backward_chunks": len(getattr(self, "_streamed_chunks", ())),
            "pending_backward_requests": len(getattr(self, "_pending_backwards", ())),
            "model_step": getattr(self, "_committed_step", None),
            "pending_groups": len(getattr(self, "_pending", [])),
            "operations": self._activities.snapshot(),
            "rollouts": self.engine.progress(),
        }

    async def _call(self, operation, function, *args, **kwargs):
        with self._activities.measure(operation):
            return await call(function, *args, **kwargs)

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
            "group_size": self.group_size,
            "groups_per_step": self.groups_per_step,
            "normalize": self.normalize,
            "validate_batch": (
                None
                if self.validate_batch is None
                else self.validate_batch.__qualname__
            ),
            "routing_replay": self.routing_replay,
            "return_expert_routing": self.engine.return_expert_routing,
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
            "loss": self.loss,
            "loss_config": self.loss_config,
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
            "base_model": getattr(self.engine.model, "base_model", None),
            "max_importance_weight": self.max_importance_weight,
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

    async def _save_state(self):
        state = {
            "version": 1,
            **self._fingerprints,
            "n": self._n,
            "submitted": self._submitted,
            "model_step": self.engine.model.step,
            "dataset_images": self._dataset_images,
            "sampling_schedule": dataclasses.asdict(self.engine.schedule),
            "base": dataclasses.asdict(self._base),
            "journal": copy.deepcopy(self._journal),
            "admitted_policy_steps": self._admitted_policy_steps.copy(),
            "active": sorted(self._active),
            "finished": sorted(self._finished),
            "received": sorted(self._received),
            "pending": [group_state(g) for g in self._pending],
            "engine": await self.engine.state_dict(),
            "eval_history": (
                [] if self.evaluator is None else self.evaluator.state_dict()
            ),
        }
        session = self._image_session()
        images = session._client._local_images if session is not None else None
        # Cancelling to_thread cannot stop the filesystem writer. Keep the
        # caller's checkpoint lock until that writer has finished, so shutdown
        # cannot race its temporary file or image pruning with the final save.
        write = asyncio.create_task(
            self._call("checkpoint_state", self._store.save, state, images=images)
        )
        try:
            await asyncio.shield(write)
        except asyncio.CancelledError:
            await write
            raise

    async def _refresh_policy(self):
        if self.engine.server_capabilities is not None:
            self.engine.server_capabilities.require("policy_versions_v1")
            if self._overlap and (
                self.normalize != "sum" or self.advantage.standardize == "batch"
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
                spans.append(
                    Span(
                        span.kind,
                        span.chunks,
                        logprobs=span.logprobs,
                        policy_step=self.engine.model.step - age,
                        run=span.run,
                        policy_version=sampled,
                        retained_kv=span.retained_kv,
                        kv_cache_policy_version=span.kv_cache_policy_version,
                        routing_handle=span.routing_handle,
                        routing_num_tokens=span.routing_num_tokens,
                    )
                )
            trajectory._spans = spans

    async def _save_weights(self):
        checkpoint = await self._call(
            "checkpoint_weights",
            self.engine.model.save_weights,
            f"rl-{self._run_key}-batch-{self._n:08d}",
            mode="training",
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
        await self._save_state()

    async def _publish_sampling_snapshot(self, *, recovering=False):
        if not self.engine._latest_snapshot_sampling:
            return
        step = self.engine.model.step
        if self._published_sampling_step == step:
            return
        # Called before new admissions, after committed training state is
        # recoverable. Existing trajectories may keep using prior snapshots.
        if self._store and not recovering:
            await self._save_state()
        checkpoint = await self._call(
            "sampling_snapshot",
            self.engine.model.save_weights,
            f"rl-{self._run_key}-sampling-{step:08d}",
            mode="inference",
            **({"immutable": True, **self._policy_guard()} if self._policy else {}),
        )
        if (
            checkpoint.step != step
            or checkpoint.checkpoint_type != "inference"
            or (self._policy is not None and checkpoint.policy_version != self._policy)
        ):
            raise RuntimeError(
                "published sampling snapshot does not match the committed policy"
            )
        self._published_sampling_step = step

    async def _periodic_checkpoint(self):
        while True:
            await asyncio.sleep(self.checkpoint.rollout_every)
            async with self._lock:
                await self._save_state()

    def _backward_kwargs(self, data, *, zero_out=True):
        recovered = all(d.get("_rl_recovered_routing", False) for d in data)
        if (
            self.routing_replay
            and not recovered
            and any(not d.get("expert_routing_handle") for d in data)
        ):
            raise ValueError(
                "routing_replay requires a routing handle for every training datum"
            )
        routing_options = (
            {"force_routing_replay": True, "compute_expert_flip_metric": True}
            if self.routing_replay
            else {}
        )
        return {
            "loss_fn": "ppo" if self.loss == "decoupled_ppo" else self.loss,
            "zero_out": zero_out,
            **routing_options,
            **self.loss_config,
            **(
                {"force_routing_replay": False, "compute_expert_flip_metric": False}
                if recovered
                else {}
            ),
            **self._policy_guard(),
        }

    @staticmethod
    def _routing_batches(data):
        # Keep fresh sampler captures enabled when a batch also contains saved
        # trajectories. Routing mode is per RPC, so split only at mode changes.
        batches = []
        for datum in data:
            if not batches or bool(datum.get("_rl_recovered_routing")) != bool(
                batches[-1][-1].get("_rl_recovered_routing")
            ):
                batches.append([])
            batches[-1].append(datum)
        return batches

    @staticmethod
    def _backward_data(data):
        return [
            {
                key: value
                for key, value in datum.items()
                if key != "_rl_recovered_routing"
                and not (
                    datum.get("_rl_recovered_routing")
                    and key.startswith("expert_routing_")
                )
            }
            for datum in data
        ]

    async def _backward(self, data, *, zero_out=True):
        batches = self._routing_batches(data)
        if len(batches) > 1:
            results = [
                await self._backward(batch, zero_out=zero_out and index == 0)
                for index, batch in enumerate(batches)
            ]
            return _merge_forward_backward_sub_batch_results(
                results, [len(b) for b in batches]
            )
        before = self.engine.model.step
        fb = await self._call(
            "backward",
            self.engine.model.forward_backward,
            self._backward_data(data),
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
            index, task, count = self._pending_backwards[0]
            if not all_pending and not task.done():
                break
            self._streamed_results[index] = await asyncio.shield(task)
            self._pending_backwards.pop(0)
            self._check_step()
        # Surface an out-of-order failure without waiting for an earlier RPC.
        for index, task, count in self._pending_backwards:
            if task.done():
                task.result()

    async def _submit_backward(self, data, group_count):
        for batch in self._routing_batches(data):
            await self._submit_backward_chunk(batch, group_count)

    async def _submit_backward_chunk(self, data, group_count):
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
            # Await submission in order, not GPU completion: seq_id and the
            # initial gradient reset must precede every later contribution.
            submission = asyncio.create_task(
                self._call(
                    "backward_submit",
                    submit,
                    self._backward_data(data),
                    **self._backward_kwargs(data, zero_out=zero_out),
                )
            )
            try:
                pending = await asyncio.shield(submission)
            except _ForwardBackwardNeedsSubBatches:
                # Preserve the existing >1-GiB upload path. Its internal
                # sub-batches must stay behind successful earlier requests.
                await self._collect_backwards(all_pending=True)
                result = await self._backward(data, zero_out=zero_out)
                self._streamed_results.append(result)
                self._streamed_chunks.append(data)
                return
            except asyncio.CancelledError as error:
                # The submit RPC can already be accepted. Recover its handle
                # before propagating cancellation so finalization can drain it.
                pending = await asyncio.shield(submission)
                cancelled = error
            index = len(self._streamed_results)
            self._streamed_results.append(None)
            task = asyncio.create_task(self._wait_backward(pending))
            self._pending_backwards.append((index, task, group_count))
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
            # The journal preserves actions/loss inputs, not durable sampler
            # routing. Never resolve its old handles, even if files still exist.
            if chunks is None:
                data = [dict(d, _rl_recovered_routing=True) for d in data]
            else:
                chunks = [
                    [dict(d, _rl_recovered_routing=True) for d in chunk]
                    for chunk in chunks
                ]
        if chunks is None:
            fb = await self._backward(data)
        else:
            results = []
            for index, chunk in enumerate(chunks):
                results.append(await self._backward(chunk, zero_out=index == 0))
            fb = _merge_forward_backward_sub_batch_results(
                results, [len(c) for c in chunks]
            )
        return fb, await self._optimize(optimizer_kwargs)

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
                groups = [g for g in self._pending if g.id not in self._streamed_groups]
                # Excluded members can force a group's baseline to use the
                # whole batch. Only these groups wait for the final rewards.
                if not flush:
                    groups = [
                        g
                        for g in groups
                        if sum(
                            value is not None
                            for value in reward_values(
                                [g.trajectories], self.truncation
                            )[0]
                        )
                        >= self.completion.min_members
                    ]
                if not groups:
                    return
                if self.forward_backward_batch is None:
                    if len(groups) < self.forward_backward_groups and not flush:
                        return
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
                        reward_values(
                            [g.trajectories for g in self._pending], self.truncation
                        ),
                        min_members=self.completion.min_members,
                    )
                    by_id = {
                        g.id: values
                        for g, values in zip(self._pending, all_values, strict=True)
                    }
                self._check_step()
                data, selected = [], []
                tokens = 0
                for group in groups:
                    self._apply_policy_provenance(group.trajectories)
                    contribution, metrics = build_batch(
                        [group.trajectories],
                        estimator=estimator,
                        normalize=self.normalize,
                        truncation=self.truncation,
                        min_members=self.completion.min_members,
                        current_step=self._committed_step,
                        max_staleness=0,
                        defer_normalization=True,
                        advantages=None if by_id is None else [by_id[group.id]],
                    )
                    if metrics["staleness/frac_masked"]:
                        raise RuntimeError(
                            "synchronous backward received stale samples"
                        )
                    data.extend(contribution)
                    selected.append(group)
                    # Advantages align with every input position, including
                    # conditioning text and expanded image tokens.
                    tokens += sum(len(d["advantages"]) for d in contribution)
                    if (
                        self.forward_backward_batch is not None
                        and self.forward_backward_batch.reached(len(data), tokens)
                    ):
                        break
                if (
                    self.forward_backward_batch is not None
                    and not self.forward_backward_batch.reached(len(data), tokens)
                    and not flush
                ):
                    # Empty groups cannot help reach a work threshold. Consume
                    # them without an RPC or resetting accumulated gradients.
                    if not data:
                        self._streamed_groups.update(g.id for g in selected)
                    return
                groups = selected
                if data:
                    if self.loss == "decoupled_ppo":
                        forward = await self._call(
                            "forward",
                            self.engine.model.forward,
                            data,
                            **self._policy_guard(),
                            loss_fn="importance_sampling",
                            logprob_temperature=self.engine.temperature,
                        )
                        data, correction = decouple_ppo(
                            data,
                            forward.logprobs,
                            max_importance_weight=self.max_importance_weight,
                        )
                        self._streamed_corrections.append(
                            (
                                sum(sum(a != 0 for a in d["advantages"]) for d in data),
                                correction,
                            )
                        )
                    await self._submit_backward(data, len(groups))
                self._streamed_groups.update(g.id for g in groups)

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

    def _batch_group_count(self):
        return min(
            self.groups_per_step, self._total_groups - self._n * self.groups_per_step
        )

    def _wait_batch(self):
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
                self.engine.accept(result)
                if result.id in self._finished:
                    return False
                unseen = [t for t in result.trajectories if t.id not in self._received]
                self._received.update(t.id for t in unseen)
                result.trajectories = unseen
                if result.final:
                    self._active.discard(result.id)
                    self._finished.add(result.id)
                    self.engine.acknowledge(result.id)
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
                    self._pending.append(result)
                return True
        finally:
            for task in (result_task, stop_task):
                if not task.done():
                    task.cancel()
            await asyncio.gather(result_task, stop_task, return_exceptions=True)

    async def run(self, dataset, *, steps: int, after_recovery=None):
        """Yield committed batches, optionally reconciling effects on recovery.

        Await ``after_recovery(completed_batches)`` after restoring weights and
        replaying committed updates, before advancing training. It also runs
        when all requested batches are already complete. Callers must make
        reconciliation idempotent; failure leaves the saved state retryable.
        """
        if self._running:
            raise RuntimeError("trainer is already running")
        _integer(steps, "steps", 1)
        rows = list(dataset)
        image_session = self._image_session()
        if not rows or steps < 1:
            raise ValueError("run requires a nonempty dataset and positive steps")
        if self.evaluator is not None:
            rows = self.evaluator.exclude_holdout(rows)
            if not rows:
                raise ValueError("no training rows remain after holdout exclusion")
        if not self.repeat_dataset and steps > math.ceil(
            len(rows) / self.groups_per_step
        ):
            raise ValueError(
                "steps exceeds the finite dataset; enable repeat_dataset to cycle"
            )
        self._total_groups = steps * self.groups_per_step
        if not self.repeat_dataset:
            self._total_groups = min(self._total_groups, len(rows))
        self._n, self._submitted = 0, 0
        self._active, self._finished, self._received = set(), set(), set()
        self._pending, self._journal = [], []
        self._admitted_policy_steps = {}
        self._base = None
        self._stop, self._lock = asyncio.Event(), asyncio.Lock()
        self._checkpoint_task = None
        self._pending_backwards = []
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
            self._fingerprints["config_fingerprint"] = fingerprint(self._config())
        self._run_key = self._fingerprints["plan_fingerprint"][:12]
        store_context = (
            StateStore(self.checkpoint) if self.checkpoint else nullcontext()
        )
        handlers = {}
        healthy = True
        recovered = 0
        self._activities = Activities()
        self._published_sampling_step = None
        self._running = True
        self._status = "running"
        try:
            with store_context as self._store:
                saved = self._store.load() if self._store else None
                if saved:
                    if self.init_checkpoint is not None:
                        raise ValueError(
                            "init_checkpoint is mutually exclusive with automatic resume"
                        )
                    if saved.get("version") != 1 or any(
                        saved.get(k) != v for k, v in self._fingerprints.items()
                    ):
                        raise ValueError(
                            "resume dataset, order, holdout, schedule, or training configuration changed"
                        )
                if self._store and image_session is not None:
                    restored = await image_session.restore_images(
                        {"rows": rows, "saved": saved}, image_store=self._store.images
                    )
                    rows, saved = restored["rows"], restored["saved"]
                from river_client.images import image_handles

                self._dataset_images = list(
                    {image.sha256: image for image in image_handles(rows)}.values()
                )
                async with self.engine:
                    sampling_before = self.engine.sampling_metrics()
                    await self._refresh_policy()
                    if saved:
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
                        for update in self._journal:
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
                        self._n, self._submitted = saved["n"], saved["submitted"]
                        self._active, self._finished, self._received = (
                            set(saved["active"]),
                            set(saved["finished"]),
                            set(saved["received"]),
                        )
                        self._pending = [
                            group_from_state(g, recovering=True)
                            for g in saved["pending"]
                        ]
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
                        self.engine.load_state_dict(saved["engine"])
                        if self.evaluator:
                            self.evaluator.load_state_dict(saved["eval_history"])
                    else:
                        if self.init_checkpoint is not None:
                            await call(
                                self.engine.model.load_weights,
                                self.init_checkpoint,
                                load_optimizer=False,
                            )
                            await self._refresh_policy()
                        if self._store:
                            await self._save_weights()
                    self._committed_step = self.engine.model.step
                    # Reconcile external effects of the last committed batch
                    # before another update, including a fully completed run.
                    if saved and after_recovery is not None:
                        await after_recovery(self._n)
                    self._validate_reservations()
                    if self.evaluator:
                        await self.evaluator.launch(self.engine.model, self._n)
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
                            batch_started = time.monotonic()
                            batch_operations = self._activities.snapshot()
                            if (
                                self._checkpoint_task is not None
                                and self._checkpoint_task.done()
                            ):
                                self._checkpoint_task.result()
                            self._check_step()
                            async with self._lock:
                                await self._publish_sampling_snapshot()
                            self._validate_reservations()
                            ahead = min(
                                self.engine.schedule.admit_ahead, self.max_staleness
                            )
                            slots = (1 + self.max_staleness) * self.groups_per_step
                            # Extra whole groups consume the same admission budget.
                            desired = min(
                                slots,
                                math.ceil(
                                    (1 + ahead)
                                    * self.groups_per_step
                                    * self.engine.schedule.oversample_factor
                                ),
                            )
                            async with self._lock:
                                while (
                                    self._submitted < self._total_groups
                                    and self._submitted
                                    < self._n * self.groups_per_step + desired
                                ):
                                    row = rows[self._submitted % len(rows)]
                                    group_id = self.engine.submit(
                                        row,
                                        group_size=self.group_size,
                                        completion=self.completion,
                                        id=f"group-{self._submitted}",
                                        priority=(
                                            self._committed_step
                                            if self.stale_policy == "wait"
                                            else 0
                                        ),
                                    )
                                    if self.stale_policy == "wait":
                                        self._admitted_policy_steps[group_id] = (
                                            self._committed_step
                                        )
                                    self._active.add(group_id)
                                    self._submitted += 1
                            wait_seconds, wait_count = 0.0, 0
                            # Restored pending groups may already have populated
                            # worker gradients in the old process. Rebuild them.
                            await self._accumulate_ready()
                            while (
                                not self._pending_ready()
                                and self._active
                                and not self._stop.is_set()
                            ):
                                blocked = (
                                    self.stale_policy == "wait"
                                    and len(self._pending) >= self.groups_per_step
                                )
                                wait_started = time.monotonic()
                                await self._receive()
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
                                data, metrics = build_batch(
                                    [g.trajectories for g in selected],
                                    estimator=self.advantage,
                                    normalize=self.normalize,
                                    truncation=self.truncation,
                                    min_members=self.completion.min_members,
                                    current_step=self.engine.model.step,
                                    max_staleness=(
                                        self.max_staleness
                                        if self.stale_policy == "mask_span"
                                        else None
                                    ),
                                )
                                if self.validate_batch is not None:
                                    await call(
                                        self.validate_batch, trajectories, metrics
                                    )
                                if data:
                                    if (
                                        self.loss == "decoupled_ppo"
                                        and not self._overlap
                                    ):
                                        forward = await self._call(
                                            "forward",
                                            self.engine.model.forward,
                                            data,
                                            **self._policy_guard(),
                                            loss_fn="importance_sampling",
                                            logprob_temperature=self.engine.temperature,
                                        )
                                        data, correction_metrics = decouple_ppo(
                                            data,
                                            forward.logprobs,
                                            max_importance_weight=self.max_importance_weight,
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
                                        )
                                        scale = accumulation_scale(
                                            [g.trajectories for g in selected],
                                            estimator=self.advantage,
                                            truncation=self.truncation,
                                            min_members=self.completion.min_members,
                                            normalize=self.normalize,
                                            metrics=metrics,
                                        )
                                        if scale != 1.0:
                                            optimizer_kwargs["gradient_scale"] = scale
                                            if "loss" in fb.metrics:
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
                                    if self._store:
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
                                if self.stale_policy == "wait":
                                    for group in selected:
                                        del self._admitted_policy_steps[group.id]
                                    self._validate_reservations()
                                self._n += 1
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
                                    and len(self._journal)
                                    >= self.checkpoint.weights_every
                                ):
                                    await self._save_weights()
                                if self.evaluator:
                                    try:
                                        await self.evaluator.launch(
                                            self.engine.model,
                                            self._n,
                                            final=self._n == steps,
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
                            yield step
                        if self.evaluator:
                            try:
                                await self._finish_evaluation()
                            except Exception:
                                # Background rollout/logging failures do not
                                # invalidate already committed training updates.
                                if self._store:
                                    async with self._lock:
                                        await self._save_state()
                                raise
                    except Exception:
                        healthy = False
                        raise
                    finally:
                        # Submitted RPCs keep running even if their waiter is
                        # cancelled. Drain before closing/checkpointing a model;
                        # failed contributions must never reach an optimizer.
                        backward_failure = None
                        if self._pending_backwards:
                            results = await asyncio.gather(
                                *(
                                    task
                                    for index, task, count in self._pending_backwards
                                ),
                                return_exceptions=True,
                            )
                            self._pending_backwards.clear()
                            failure = next(
                                (r for r in results if isinstance(r, BaseException)),
                                None,
                            )
                            if failure is not None and healthy:
                                healthy = False
                                backward_failure = failure
                        if self._backward_executor is not None:
                            self._backward_executor.shutdown(wait=True)
                            self._backward_executor = None
                        if self._checkpoint_task:
                            self._checkpoint_task.cancel()
                            result = await asyncio.gather(
                                self._checkpoint_task, return_exceptions=True
                            )
                            if isinstance(result[0], Exception):
                                healthy = False
                                raise result[0]
                        if self._store and healthy and not self._updating:
                            async with self._lock:
                                if self._n == steps and self._journal:
                                    await self._save_weights()
                                else:
                                    await self._save_state()
                        if self.evaluator:
                            await self.evaluator.close()
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
            if self._status == "running":
                self._status = "completed" if self._n == steps else "stopped"
            for sig, handler in handlers.items():
                asyncio.get_running_loop().remove_signal_handler(sig)
                signal.signal(sig, handler)
            self._running = False


def run(trainer: AsyncTrainer, dataset, *, steps: int, on_step=None):
    """Synchronous entry point; notebooks should use ``async for`` directly."""

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
