"""Checkpoint-pinned evaluation with separate sessions and measured-step logging."""

from __future__ import annotations

import asyncio
from dataclasses import asdict, dataclass
from functools import partial

import numpy as np

from river_client.types import Checkpoint

from .checkpoint import fingerprint
from .config import GroupCompletion
from .engine import call


class CheckpointSampler:
    """Sample from a saved checkpoint on a separate evaluation session.

    Attributes:
        step: Training step recorded by the checkpoint.
        submit_sampling_batch: Batch submission bound to this checkpoint.
    """

    def __init__(self, session, *, base_model, checkpoint: Checkpoint, tokenizer):
        """Bind evaluation sampling to a specific saved policy.

        Args:
            session: Session allocated for evaluation.
            base_model: Model used to create the checkpoint.
            checkpoint: Saved weights and training step to evaluate.
            tokenizer: Tokenizer used to decode evaluation samples.
        """
        if not isinstance(checkpoint, Checkpoint):
            raise TypeError(
                "evaluation requires a saved Checkpoint with a recorded step"
            )
        self.session, self.base_model = session, base_model
        self.checkpoint, self.tokenizer = checkpoint, tokenizer

    def get_server_capabilities(self):
        # Custom session adapters own their protocol contract. Native River
        # sessions expose the same preflight as a training Model.
        read = getattr(self.session, "get_server_capabilities", None)
        return read(model_name=self.base_model) if read is not None else None

    @property
    def step(self):
        return self.checkpoint.step

    def sample(self, **kwargs):
        return self.session.sample(
            base_model=self.base_model,
            checkpoint=self.checkpoint,
            tokenizer=self.tokenizer,
            **kwargs,
        )

    def submit_sample(self, **kwargs):
        return self.session.submit_sample(
            base_model=self.base_model,
            checkpoint=self.checkpoint,
            tokenizer=self.tokenizer,
            **kwargs,
        )

    @property
    def submit_sampling_batch(self):
        return partial(
            self.session.submit_sampling_batch,
            base_model=self.base_model,
            checkpoint=self.checkpoint,
            tokenizer=self.tokenizer,
        )


@dataclass
class Evaluation:
    """Metrics and trajectories from evaluating one checkpoint variant.

    Attributes:
        step: Training step represented by the checkpoint.
        variant: Name of the evaluation configuration.
        checkpoint: Saved weights sampled by this evaluation.
        metrics: Aggregate evaluation measurements.
        trajectories: Individual evaluation rollouts.
    """

    step: int
    variant: str
    checkpoint: Checkpoint
    metrics: dict[str, float]
    trajectories: list


class Evaluator:
    """Run a holdout evaluation against saved model checkpoints.

    Each variant uses a separate rollout engine built from a
    ``CheckpointSampler``. Evaluation can continue while the training model
    advances; allocate its session on evaluation capacity.

    Attributes:
        holdout: Dataset rows reserved for evaluation.
        variants: Names of evaluation configurations.
        results: Completed evaluation results.
    """

    def __init__(
        self,
        holdout,
        *,
        engine_factory,
        every=20,
        group_size=4,
        final_group_size=8,
        variants=("default",),
        sink=None,
    ):
        """Configure the holdout, cadence, and evaluation variants.

        Args:
            holdout: Rows reserved for evaluation and excluded from training.
            engine_factory: Callable ``(checkpoint, variant)`` returning an
                evaluation rollout engine.
            every: Training batches between periodic evaluations; zero
                disables periodic evaluation.
            group_size: Samples per holdout row in periodic evaluations.
            final_group_size: Samples per row in the final evaluation.
            variants: Named evaluation configurations to run per checkpoint.
            sink: Optional callback receiving each ``Evaluation`` result.
        """
        if min(every, final_group_size) < 0 or group_size < 1 or not variants:
            raise ValueError(
                "evaluation cadences must be nonnegative, group_size positive, and variants nonempty"
            )
        self.holdout = list(holdout)
        if not self.holdout:
            raise ValueError("evaluation holdout must be nonempty")
        self.engine_factory, self.sink = engine_factory, sink
        self.every, self.group_size, self.final_group_size = (
            every,
            group_size,
            final_group_size,
        )
        self.variants = tuple(variants)
        if len(set(self.variants)) != len(self.variants):
            raise ValueError("evaluation variants must be unique")
        self.results: list[Evaluation] = []
        self._jobs = {}
        self._tasks = []

    def config_dict(self):
        return {
            "holdout": self.holdout,
            "every": self.every,
            "group_size": self.group_size,
            "final_group_size": self.final_group_size,
            "variants": self.variants,
        }

    def exclude_holdout(self, rows):
        excluded = {fingerprint(row) for row in self.holdout}
        return [row for row in rows if fingerprint(row) not in excluded]

    async def launch(self, model, step, *, final=False):
        # Surface failures promptly, even if the next eval is not due yet.
        for task in self._tasks:
            if task.done():
                task.result()
        use_final = final and self.final_group_size > 0
        if not use_final and (not self.every or step % self.every):
            return
        if str(step) in self._jobs:
            return
        # Unfinished jobs persist in trainer state and may resume after a long pause.
        checkpoint = await call(
            model.save_weights, f"rl-eval-{step:08d}", mode="inference"
        )
        self._jobs[str(step)] = {
            "checkpoint": asdict(checkpoint),
            "group_size": self.final_group_size if use_final else self.group_size,
            "done": [],
        }
        self._start(step)

    def _start(self, step):
        job = self._jobs[str(step)]
        for variant in self.variants:
            if variant not in job["done"]:
                self._tasks.append(asyncio.create_task(self._evaluate(step, variant)))

    async def _evaluate(self, step, variant):
        job = self._jobs[str(step)]
        checkpoint = Checkpoint(**job["checkpoint"])
        engine = self.engine_factory(checkpoint, variant)
        if (
            not isinstance(engine.model, CheckpointSampler)
            or engine.model.checkpoint != checkpoint
        ):
            raise ValueError(
                "evaluation engines must use CheckpointSampler pinned to the measured checkpoint"
            )
        trajectories = []
        async for group in engine.rollout(
            self.holdout,
            group_size=job["group_size"],
            completion=GroupCompletion(mode="wait", min_members=1),
        ):
            trajectories.extend(group)
        metrics = {
            "reward_mean": float(np.mean([t.reward for t in trajectories])),
            "reward_std": float(np.std([t.reward for t in trajectories])),
            "generated_tokens_mean": float(
                np.mean([t.generated_tokens for t in trajectories])
            ),
            "truncated_frac": sum(t.truncated is not None for t in trajectories)
            / len(trajectories),
        }
        result = Evaluation(step, variant, checkpoint, metrics, trajectories)
        if self.sink:
            await call(self.sink, result)
        self.results.append(result)
        job["done"].append(variant)

    async def wait(self):
        if self._tasks:
            await asyncio.gather(*self._tasks)

    async def close(self):
        for task in self._tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)

    def state_dict(self):
        return self._jobs

    def load_state_dict(self, state):
        self._jobs = state
        for step in state:
            self._start(int(step))


class WandbSink:
    """Log evaluation metrics and sampled trajectories to a W&B run.

    Metrics use the evaluated checkpoint's step, even if an evaluation
    finishes after newer training batches.
    """

    def __init__(self, run, *, table_samples=8):
        """Configure the W&B run and number of trajectories shown per result.

        Args:
            run: Active W&B run.
            table_samples: Maximum trajectories to include in the sample table.
        """
        self.run, self.table_samples = run, table_samples
        run.define_metric("eval/step")
        run.define_metric("eval/*", step_metric="eval/step")

    def __call__(self, result):
        import json

        import wandb

        table = wandb.Table(
            columns=["reward", "turns", "tool_calls", "transcript"],
            data=[
                [
                    t.reward,
                    t.turns,
                    t.metrics.get("tool_calls", 0),
                    json.dumps(
                        t.messages,
                        ensure_ascii=False,
                        default=lambda value: f"<{type(value).__name__}>",
                    ),
                ]
                for t in result.trajectories[: self.table_samples]
            ],
        )
        self.run.log(
            {
                "eval/step": result.step,
                **{f"eval/{result.variant}/{k}": v for k, v in result.metrics.items()},
                f"eval/{result.variant}/trajectories": table,
            }
        )
