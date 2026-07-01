"""Tinker-based reinforcement learning runtimes.

This module provides a small hosted-training-oriented RL runtime surface for
Tinker. Async training is organized around rollout groups:

- ``one_step_off_async`` keeps a single future rollout group in flight, which
  bounds policy staleness to one training step.
- ``fully_async`` widens the same pipeline to multiple queued rollout groups,
  allowing bounded off-policy training with explicit staleness control.
"""

from __future__ import annotations

import os
from collections import deque
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Literal, Protocol

TinkerRLExecutionMode = Literal["sync", "one_step_off_async", "fully_async"]


@dataclass
class TinkerRLConfig:
    """Configuration for Tinker-based RL training."""

    base_model: str = "meta-llama/Llama-3.1-8B-Instruct"
    algorithm: Literal["importance_sampling", "ppo"] = "importance_sampling"
    lora_rank: int = 16
    steps: int = 1
    num_rollouts: int = 8
    batch_size: int = 8
    learning_rate: float = 1e-4
    weight_sync_interval: int = 1
    checkpoint_interval: int = 1
    max_new_tokens: int = 128
    temperature: float = 0.0
    stop: list[str] = field(default_factory=list)
    execution_mode: TinkerRLExecutionMode = "sync"
    max_steps_off_policy: int = 1

    def __post_init__(self) -> None:
        """Validate RL configuration."""
        if self.algorithm not in {"importance_sampling", "ppo"}:
            raise ValueError("algorithm must be importance_sampling or ppo")
        if self.execution_mode not in {"sync", "one_step_off_async", "fully_async"}:
            raise ValueError(
                "execution_mode must be sync, one_step_off_async, or fully_async"
            )
        if self.lora_rank <= 0:
            raise ValueError("lora_rank must be positive")
        if self.steps <= 0:
            raise ValueError("steps must be positive")
        if self.num_rollouts <= 0:
            raise ValueError("num_rollouts must be positive")
        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be positive")
        if self.weight_sync_interval <= 0:
            raise ValueError("weight_sync_interval must be positive")
        if self.checkpoint_interval <= 0:
            raise ValueError("checkpoint_interval must be positive")
        if self.max_new_tokens <= 0:
            raise ValueError("max_new_tokens must be positive")
        if self.temperature < 0:
            raise ValueError("temperature must be non-negative")
        if self.max_steps_off_policy <= 0:
            raise ValueError("max_steps_off_policy must be positive")
        if (
            self.execution_mode == "one_step_off_async"
            and self.max_steps_off_policy != 1
        ):
            raise ValueError(
                "one_step_off_async currently supports max_steps_off_policy=1 only"
            )


@dataclass
class TinkerRLRolloutGroup:
    """One generated group of RL rollouts ready for training."""

    generation_step: int
    model_version: int
    scheduled_at_training_step: int
    datums: list[Any]
    rewards: list[float]

    @property
    def num_rollouts(self) -> int:
        """Number of rollouts represented by the group."""
        return len(self.rewards)


@dataclass
class TinkerRLTrainingResult:
    """Summary returned by the Tinker RL runtime."""

    metrics: dict[str, int | float]
    checkpoints: list[str]


class RolloutGroupGenerator(Protocol):
    """Callable that generates one rollout group for RL training."""

    def __call__(
        self,
        *,
        sampling_client: Any,
        tokenizer: Any,
        generation_step: int,
        model_version: int,
        scheduled_at_training_step: int,
    ) -> TinkerRLRolloutGroup: ...


def train_tinker_rl(
    *,
    tinker: Any,
    config: TinkerRLConfig,
    job_id: str,
    generate_group: RolloutGroupGenerator,
    callback: Any | None = None,
) -> TinkerRLTrainingResult:
    """Train a Tinker RL job using the configured execution mode.

    ``callback`` is an optional ``TrainingCallback``-shaped object
    (``on_step_end(step, state, metrics)`` + ``on_checkpoint(idx, path,
    state)``) used by the HTTP-push runtime to stream per-step rewards and
    checkpoint paths back to the platform. RL has no ``TrainingState`` — it
    passes ``None`` for the state argument; callbacks should treat it as
    advisory context only.
    """

    service_client = tinker.ServiceClient(base_url=os.environ.get("TINKER_BASE_URL"))
    training_client = service_client.create_lora_training_client(
        base_model=config.base_model,
        rank=config.lora_rank,
    )
    tokenizer = training_client.get_tokenizer()
    adam_params = tinker.AdamParams(
        learning_rate=config.learning_rate,
        beta1=0.9,
        beta2=0.95,
        eps=1e-8,
    )
    if config.execution_mode in {"one_step_off_async", "fully_async"}:
        return _train_async_pipeline(
            training_client=training_client,
            tokenizer=tokenizer,
            adam_params=adam_params,
            config=config,
            job_id=job_id,
            generate_group=generate_group,
            callback=callback,
        )
    return _train_sync(
        training_client=training_client,
        tokenizer=tokenizer,
        adam_params=adam_params,
        config=config,
        job_id=job_id,
        generate_group=generate_group,
        callback=callback,
    )


def _emit_step_metrics(
    callback: Any | None,
    *,
    step: int,
    step_rewards: list[float],
    extra: dict[str, float] | None = None,
) -> None:
    """Forward per-step reward statistics to the HTTP-push callback.

    Shapes the metrics dict into the ``train/<suffix>`` keys the
    ``ProgressPushCallback`` rewrites into axis-step series. Silent if no
    callback is installed (legacy paths that set it to None).
    """
    if callback is None or not step_rewards:
        return
    metrics: dict[str, float] = {
        "train/reward": float(sum(step_rewards) / len(step_rewards)),
        "train/reward_max": float(max(step_rewards)),
        "train/reward_min": float(min(step_rewards)),
    }
    if extra:
        metrics.update(extra)
    try:
        callback.on_step_end(step, None, metrics)
    except Exception:
        pass


def _emit_checkpoint(
    callback: Any | None, *, step: int, path: str
) -> None:
    if callback is None:
        return
    try:
        callback.on_checkpoint(step, path, None)
    except Exception:
        pass


def _train_sync(
    *,
    training_client: Any,
    tokenizer: Any,
    adam_params: Any,
    config: TinkerRLConfig,
    job_id: str,
    generate_group: RolloutGroupGenerator,
    callback: Any | None = None,
) -> TinkerRLTrainingResult:
    """Run synchronous RL training."""

    checkpoint_paths: list[str] = []
    reward_history: list[float] = []
    reward_history_per_step: list[list[float]] = []
    model_version = 0
    last_synced_model_version = 0
    weight_sync_count = 0
    sampling_client: Any | None = None

    for step in range(1, config.steps + 1):
        if sampling_client is None or (step - 1) % config.weight_sync_interval == 0:
            model_version += 1
            sampling_client = training_client.save_weights_and_get_sampling_client(
                name=f"training-job-{job_id}-step-{step}"
            )
            last_synced_model_version = model_version
            weight_sync_count += 1

        group = generate_group(
            sampling_client=sampling_client,
            tokenizer=tokenizer,
            generation_step=step,
            model_version=model_version,
            scheduled_at_training_step=step - 1,
        )
        _require_datums(group)
        training_client.forward_backward(group.datums, loss_fn=config.algorithm).result()
        training_client.optim_step(adam_params).result()

        # Keep both the flattened and per-step shapes:
        # - flat `reward_history` still drives the scalar mean/max/min summary
        # - per-step buckets drive the series the UI charts off metrics_contract
        step_rewards = list(group.rewards)
        reward_history.extend(step_rewards)
        reward_history_per_step.append(step_rewards)
        _emit_step_metrics(
            callback,
            step=step,
            step_rewards=step_rewards,
            extra={
                "train/model_version": float(model_version),
                "train/weight_sync_count": float(weight_sync_count),
            },
        )
        if step % config.checkpoint_interval == 0:
            checkpoint = training_client.save_weights_for_sampler(
                f"training-job-{job_id}-step-{step}"
            ).result()
            checkpoint_paths.append(checkpoint.path)
            _emit_checkpoint(callback, step=step, path=checkpoint.path)

    if not checkpoint_paths:
        checkpoint = training_client.save_weights_for_sampler(
            f"training-job-{job_id}-final"
        ).result()
        checkpoint_paths.append(checkpoint.path)

    return TinkerRLTrainingResult(
        metrics=_build_training_metrics(
            reward_history=reward_history,
            reward_history_per_step=reward_history_per_step,
            steps=config.steps,
            generation_step=config.steps,
            training_step=config.steps,
            model_version=model_version,
            last_synced_model_version=last_synced_model_version,
            weight_sync_count=weight_sync_count,
            max_staleness_observed=0,
        ),
        checkpoints=checkpoint_paths,
    )


def _train_async_pipeline(
    *,
    training_client: Any,
    tokenizer: Any,
    adam_params: Any,
    config: TinkerRLConfig,
    job_id: str,
    generate_group: RolloutGroupGenerator,
    callback: Any | None = None,
) -> TinkerRLTrainingResult:
    """Run bounded async RL training over queued rollout groups."""

    checkpoint_paths: list[str] = []
    reward_history: list[float] = []
    reward_history_per_step: list[list[float]] = []
    training_step = 0
    generation_step = 0
    model_version = 1
    last_synced_model_version = model_version
    weight_sync_count = 1
    max_staleness_observed = 0

    sampling_client = training_client.save_weights_and_get_sampling_client(
        name=f"training-job-{job_id}-step-1"
    )
    current_group = generate_group(
        sampling_client=sampling_client,
        tokenizer=tokenizer,
        generation_step=1,
        model_version=model_version,
        scheduled_at_training_step=0,
    )
    generation_step = 1
    next_generation_step = 2
    pending_groups: deque[Future[TinkerRLRolloutGroup]] = deque()
    max_pending_generation_groups = 0

    with ThreadPoolExecutor(max_workers=max(1, config.max_steps_off_policy)) as executor:
        for step in range(1, config.steps + 1):
            while (
                next_generation_step <= config.steps
                and len(pending_groups) < config.max_steps_off_policy
            ):
                pending_groups.append(
                    executor.submit(
                        generate_group,
                        sampling_client=sampling_client,
                        tokenizer=tokenizer,
                        generation_step=next_generation_step,
                        model_version=model_version,
                        scheduled_at_training_step=step,
                    )
                )
                generation_step = max(generation_step, next_generation_step)
                next_generation_step += 1
                max_pending_generation_groups = max(
                    max_pending_generation_groups,
                    len(pending_groups),
                )

            _require_datums(current_group)
            forward_backward_future = training_client.forward_backward(
                current_group.datums,
                loss_fn=config.algorithm,
            )
            optim_step_future = training_client.optim_step(adam_params)
            forward_backward_future.result()
            optim_step_future.result()

            training_step = step
            step_rewards = list(current_group.rewards)
            reward_history.extend(step_rewards)
            reward_history_per_step.append(step_rewards)
            staleness = step - current_group.scheduled_at_training_step
            max_staleness_observed = max(max_staleness_observed, staleness)
            # Async-pipeline tells you more than sync does — surface the
            # generation/training divergence, queue depth, and weight-sync
            # counter per step so the UI can show where the pipeline is
            # bottlenecked in real time (not just at the end).
            _emit_step_metrics(
                callback,
                step=step,
                step_rewards=step_rewards,
                extra={
                    "train/staleness": float(staleness),
                    "train/generation_step": float(generation_step),
                    "train/pending_generation_groups": float(len(pending_groups)),
                    "train/model_version": float(model_version),
                    "train/weight_sync_count": float(weight_sync_count),
                },
            )

            if step % config.checkpoint_interval == 0:
                checkpoint = training_client.save_weights_for_sampler(
                    f"training-job-{job_id}-step-{step}"
                ).result()
                checkpoint_paths.append(checkpoint.path)
                _emit_checkpoint(callback, step=step, path=checkpoint.path)

            if not pending_groups:
                continue

            next_group = pending_groups.popleft().result()
            if step % config.weight_sync_interval == 0:
                model_version += 1
                sampling_client = training_client.save_weights_and_get_sampling_client(
                    name=f"training-job-{job_id}-step-{step + 1}"
                )
                last_synced_model_version = model_version
                weight_sync_count += 1
            current_group = next_group

    if not checkpoint_paths:
        checkpoint = training_client.save_weights_for_sampler(
            f"training-job-{job_id}-final"
        ).result()
        checkpoint_paths.append(checkpoint.path)

    return TinkerRLTrainingResult(
        metrics=_build_training_metrics(
            reward_history=reward_history,
            reward_history_per_step=reward_history_per_step,
            steps=config.steps,
            generation_step=generation_step,
            training_step=training_step,
            model_version=model_version,
            last_synced_model_version=last_synced_model_version,
            weight_sync_count=weight_sync_count,
            max_staleness_observed=max_staleness_observed,
            max_pending_generation_groups=max_pending_generation_groups,
        ),
        checkpoints=checkpoint_paths,
    )


def _require_datums(group: TinkerRLRolloutGroup) -> None:
    """Ensure a generated rollout group contains trainable datums."""

    if group.datums:
        return
    raise RuntimeError("No RL rollouts were generated for training")


def _build_training_metrics(
    *,
    reward_history: list[float],
    reward_history_per_step: list[list[float]] | None = None,
    steps: int,
    generation_step: int,
    training_step: int,
    model_version: int,
    last_synced_model_version: int,
    weight_sync_count: int,
    max_staleness_observed: int,
    max_pending_generation_groups: int = 0,
) -> dict[str, Any]:
    """Return hosted-job-friendly RL metrics.

    Scalars summarize the whole run (mean/max/min over all rollouts; total
    tokens; async pipelining state). Series keyed under the ``steps`` axis
    turn into UI charts — see ``docs/metrics_contract.md`` for the rule the
    frontend uses to discover them.

    ``reward_history_per_step`` is optional so pre-refactor callers that only
    have the flattened ``reward_history`` still produce valid metrics (just
    without the per-step arrays). New callers should always pass it.
    """

    reward_mean = (
        float(sum(reward_history) / len(reward_history)) if reward_history else 0.0
    )
    reward_max = float(max(reward_history)) if reward_history else 0.0
    reward_min = float(min(reward_history)) if reward_history else 0.0
    metrics: dict[str, Any] = {
        "train/steps": steps,
        "train/num_rollouts": len(reward_history),
        "train/reward_mean": reward_mean,
        "train/reward_max": reward_max,
        "train/reward_min": reward_min,
        "async/generation_step": generation_step,
        "async/training_step": training_step,
        "async/model_version": model_version,
        "async/last_synced_model_version": last_synced_model_version,
        "async/weight_sync_count": weight_sync_count,
        "async/max_staleness_observed": max_staleness_observed,
        "async/max_pending_generation_groups": max_pending_generation_groups,
    }

    # Per-step series — axis + train/reward{_mean,_max,_min} arrays. Emitted
    # only when the caller provided the per-step bucketing. Mean over an
    # empty step (no rollouts that step) yields 0.0; UI will render the dip.
    if reward_history_per_step is not None and reward_history_per_step:
        non_empty_idx = [i for i, g in enumerate(reward_history_per_step) if g]
        if non_empty_idx:
            axis = [i + 1 for i in range(len(reward_history_per_step))]

            def _mean(group: list[float]) -> float:
                return float(sum(group) / len(group)) if group else 0.0

            def _safe_max(group: list[float]) -> float:
                return float(max(group)) if group else 0.0

            def _safe_min(group: list[float]) -> float:
                return float(min(group)) if group else 0.0

            metrics["steps"] = axis
            metrics["train/reward"] = [_mean(g) for g in reward_history_per_step]
            metrics["train/reward_max_per_step"] = [
                _safe_max(g) for g in reward_history_per_step
            ]
            metrics["train/reward_min_per_step"] = [
                _safe_min(g) for g in reward_history_per_step
            ]

    return metrics


__all__ = [
    "RolloutGroupGenerator",
    "TinkerRLConfig",
    "TinkerRLExecutionMode",
    "TinkerRLRolloutGroup",
    "TinkerRLTrainingResult",
    "train_tinker_rl",
]
