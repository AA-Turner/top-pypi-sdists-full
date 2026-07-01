"""Tinker-based SFT trainer implementation.

This module provides the TinkerSFTTrainer class for supervised fine-tuning
of language models using the Tinker framework with LoRA adapters.

Usage:
    from dreadnode.training.tinker import TinkerSFTTrainer, TinkerSFTConfig

    config = TinkerSFTConfig(
        base_model="meta-llama/Llama-3.1-8B-Instruct",
        steps=100,
        lora_rank=16,
    )

    trainer = TinkerSFTTrainer(config)
    trainer.train(train_data)
"""

from __future__ import annotations

import math
import tempfile
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol

import numpy as np
from loguru import logger

if TYPE_CHECKING:
    from collections.abc import Sequence

    import tinker
    from tinker import types

    from .config import TinkerSFTConfig


class TrainingCallback(Protocol):
    """Protocol for Tinker training callbacks."""

    def on_step_start(self, step: int, state: TrainingState) -> None:
        """Called at the start of each training step."""
        ...

    def on_step_end(self, step: int, state: TrainingState, metrics: dict[str, float]) -> None:
        """Called at the end of each training step."""
        ...

    def on_checkpoint(
        self, checkpoint_num: int, checkpoint_path: str, state: TrainingState
    ) -> None:
        """Called after saving a checkpoint."""
        ...

    def on_evaluation(self, state: TrainingState, metrics: dict[str, float]) -> None:
        """Called after evaluation."""
        ...


@dataclass
class TrainingState:
    """Current state of Tinker SFT training."""

    step: int = 0
    """Current training step (1-indexed during training)."""

    total_steps: int = 0
    """Total number of training steps."""

    epoch: int = 0
    """Number of full passes over the training data completed so far."""

    total_tokens_processed: int = 0
    """Total tokens processed during training."""

    total_sequences_processed: int = 0
    """Total sequences processed during training."""

    best_loss: float = float("inf")
    """Best training loss achieved."""

    started_at: datetime | None = None
    """Training start time."""

    losses: list[float] = field(default_factory=list)
    """List of per-step losses."""

    checkpoints: list[str] = field(default_factory=list)
    """List of saved checkpoint paths."""

    def elapsed_seconds(self) -> float:
        """Return seconds elapsed since training started."""
        if self.started_at is None:
            return 0.0
        return (datetime.now() - self.started_at).total_seconds()


class TinkerSFTTrainer:
    """Trainer for supervised fine-tuning using Tinker with LoRA.

    This trainer provides:
    - LoRA-based fine-tuning via Tinker service
    - Checkpoint saving and artifact logging
    - Optional sampling after training
    - Integration with Dreadnode for experiment tracking

    Example:
        # Create configuration
        config = TinkerSFTConfig(
            base_model="meta-llama/Llama-3.1-8B-Instruct",
            steps=100,
            lora_rank=16,
        )

        # Create trainer
        trainer = TinkerSFTTrainer(config)

        # Train
        state = trainer.train(train_data)
        print(f"Final loss: {state.losses[-1]:.4f}")
    """

    def __init__(
        self,
        config: TinkerSFTConfig,
        training_client: tinker.TrainingClient | None = None,
        service_client: tinker.ServiceClient | None = None,
        callbacks: Sequence[TrainingCallback] | None = None,
    ) -> None:
        """Initialize the Tinker SFT trainer.

        Args:
            config: Training configuration.
            training_client: Optional pre-initialized Tinker training client.
            service_client: Optional pre-initialized Tinker service client.
            callbacks: Optional list of training callbacks.
        """
        self.config = config
        self.callbacks = list(callbacks) if callbacks else []
        self.state = TrainingState(total_steps=config.steps or 0)

        self._training_client = training_client
        self._service_client = service_client
        self._tokenizer: Any = None
        self._renderer: Any = None
        self._adam_params: Any = None
        self._rng = np.random.default_rng(config.seed)
        self._initialized = False
        # Shuffle-without-replacement sampler state (see ``_select_batch``).
        self._epoch_order: list[int] = []
        self._epoch_pos = 0
        self._steps_per_epoch = 0

    def _initialize(self) -> None:
        """Initialize Tinker clients if not already done."""
        if self._initialized:
            return

        import tinker

        if self._service_client is None:
            self._service_client = tinker.ServiceClient(base_url=self.config.base_url)

        if self._training_client is None:
            self._training_client = self._service_client.create_lora_training_client(
                base_model=self.config.base_model,
                rank=self.config.lora_rank,
            )

        self._tokenizer = self._training_client.get_tokenizer()

        from .renderer import get_renderer

        self._renderer = get_renderer(self.config.base_model, self._tokenizer)

        self._adam_params = tinker.AdamParams(
            learning_rate=self.config.learning_rate,
            beta1=self.config.adam_beta1,
            beta2=self.config.adam_beta2,
            eps=self.config.adam_eps,
        )
        self._initialized = True

    @property
    def tokenizer(self) -> Any:
        """Get the tokenizer (initializes clients if needed)."""
        self._initialize()
        return self._tokenizer

    @property
    def renderer(self) -> Any:
        """Get the model-specific renderer (initializes clients if needed)."""
        self._initialize()
        return self._renderer

    @property
    def training_client(self) -> tinker.TrainingClient:
        """Get the training client (initializes clients if needed)."""
        self._initialize()
        return self._training_client

    @property
    def service_client(self) -> tinker.ServiceClient:
        """Get the service client (initializes clients if needed)."""
        self._initialize()
        return self._service_client

    def _resolve_total_steps(self, num_examples: int) -> int:
        """Resolve the optimizer-step budget from ``epochs`` / ``steps``.

        ``epochs`` is the primary training-length knob: one epoch is the
        number of optimizer steps needed to process every example once, i.e.
        ``ceil(num_examples / (batch_size * gradient_accumulation_steps))``.
        ``steps`` acts as a hard cap (a compute budget); when both are set the
        smaller wins, and a warning is emitted if the cap truncates the
        requested epochs. When neither is set, training defaults to one epoch.

        Also records ``steps_per_epoch`` for this run.
        """
        effective_batch = max(
            1, self.config.batch_size * self.config.gradient_accumulation_steps
        )
        self._steps_per_epoch = max(1, math.ceil(num_examples / effective_batch))

        epochs = self.config.epochs
        max_steps = self.config.steps
        if epochs is None and max_steps is None:
            epochs = 1

        if epochs is not None:
            epoch_steps = epochs * self._steps_per_epoch
            if max_steps is not None and max_steps < epoch_steps:
                logger.warning(
                    "max steps ({}) is below the {} steps needed to complete "
                    "{} epoch(s) over {} examples (effective batch {}); "
                    "training will stop after {} steps, short of the requested "
                    "epochs.",
                    max_steps,
                    epoch_steps,
                    epochs,
                    num_examples,
                    effective_batch,
                    max_steps,
                )
                return max_steps
            return epoch_steps

        # steps-only path: a pure compute budget. ``max_steps`` is guaranteed
        # non-None here (the both-None case defaulted ``epochs`` to 1 above).
        return max_steps if max_steps is not None else self._steps_per_epoch

    def train(
        self,
        train_data: list[types.Datum],
        eval_data: list[types.Datum] | None = None,
        log_to_dreadnode: bool = True,
    ) -> TrainingState:
        """Run supervised fine-tuning.

        Args:
            train_data: Training data as Tinker Datum objects.
            eval_data: Optional evaluation data.
            log_to_dreadnode: Whether to log metrics to Dreadnode.

        Returns:
            Final training state.

        Raises:
            ValueError: If training data is empty.
        """
        self._initialize()

        if not train_data:
            raise ValueError("Training dataset is empty.")

        total_steps = self._resolve_total_steps(len(train_data))
        self.state = TrainingState(total_steps=total_steps)
        self.state.started_at = datetime.now()
        # Reset the shuffle-without-replacement sampler for this run.
        self._epoch_order = []
        self._epoch_pos = 0

        if log_to_dreadnode:
            self._log_training_start(train_data, eval_data)

        # Training loop with checkpointing
        checkpoint_interval = self.config.checkpoint_interval
        step = 1

        try:
            while step <= total_steps:
                checkpoint_start = step
                checkpoint_end = min(step + checkpoint_interval - 1, total_steps)
                checkpoint_num = (step - 1) // checkpoint_interval + 1

                self._run_checkpoint(
                    train_data,
                    checkpoint_num,
                    checkpoint_start,
                    checkpoint_end,
                    log_to_dreadnode,
                )

                step = checkpoint_end + 1

        except KeyboardInterrupt:
            pass

        # Final evaluation
        if eval_data:
            self.evaluate(eval_data, step=total_steps, log_to_dreadnode=log_to_dreadnode)

        # Final checkpoint
        self.save_checkpoint("final")

        # Final sampling
        if not self.config.skip_sample and self.config.sample_prompt:
            self.sample()

        if log_to_dreadnode:
            self._log_training_end()

        return self.state

    def _run_checkpoint(
        self,
        train_data: list[types.Datum],
        checkpoint_num: int,
        start_step: int,
        end_step: int,
        log_to_dreadnode: bool,
    ) -> None:
        """Run training for one checkpoint interval."""
        import dreadnode as dn

        if log_to_dreadnode:
            with dn.task_span(
                f"checkpoint-{checkpoint_num}",
                tags=["checkpoint", "training"],
            ) as task:
                stats = self._train_steps(train_data, start_step, end_step, log_to_dreadnode)
                self._log_checkpoint_stats(task, start_step, end_step, stats)

                checkpoint_name = f"checkpoint-{checkpoint_num}-step{end_step}"
                checkpoint_path = self._save_checkpoint_internal(checkpoint_name)
                task.log_output("checkpoint_path", checkpoint_path)

                if not self.config.skip_sample and self.config.sample_prompt:
                    samples = self._sample_internal()
                    task.log_output("samples", samples)
        else:
            stats = self._train_steps(train_data, start_step, end_step, log_to_dreadnode)
            checkpoint_name = f"checkpoint-{checkpoint_num}-step{end_step}"
            self._save_checkpoint_internal(checkpoint_name)

    def _train_steps(
        self,
        train_data: list[types.Datum],
        start_step: int,
        end_step: int,
        log_to_dreadnode: bool,
    ) -> dict[str, Any]:
        """Train for a range of steps."""
        from dreadnode.tracing.span import TaskSpan
        from dreadnode.training.events import TrainingStepCompleted

        losses = []
        total_tokens = 0
        total_sequences = 0

        for current_step in range(start_step, end_step + 1):
            self.state.step = current_step

            # Notify callbacks
            for callback in self.callbacks:
                callback.on_step_start(current_step, self.state)

            # Accumulate the loss components (not per-micro-batch means) so the
            # logged step loss is the exact token-weighted mean across the whole
            # step. Micro-batches can differ in size when the sampler returns a
            # partial final batch at an epoch boundary; averaging means would
            # over-weight those small batches.
            step_neg_weighted_logprobs = 0.0
            step_weights = 0.0
            token_count = 0
            sequence_count = 0
            for _ in range(self.config.gradient_accumulation_steps):
                batch = self._select_batch(train_data)
                fwd_bwd_result = self._training_client.forward_backward(
                    batch, loss_fn="cross_entropy"
                ).result()
                neg_weighted_logprobs, weights = _weighted_loss_components(
                    batch, fwd_bwd_result.loss_fn_outputs
                )
                step_neg_weighted_logprobs += neg_weighted_logprobs
                step_weights += weights
                token_count += sum(d.model_input.length for d in batch)
                sequence_count += len(batch)
            self._training_client.optim_step(self._adam_params).result()

            loss = (
                float(step_neg_weighted_logprobs / step_weights)
                if step_weights
                else float("nan")
            )

            # Update state
            self.state.total_tokens_processed += token_count
            self.state.total_sequences_processed += sequence_count
            self.state.losses.append(loss)
            self.state.best_loss = min(self.state.best_loss, loss)
            # Completed epochs = how many full passes over the data the
            # examples seen so far amount to.
            num_examples = len(train_data)
            if num_examples > 0:
                self.state.epoch = self.state.total_sequences_processed // num_examples

            losses.append(loss)
            total_tokens += token_count
            total_sequences += sequence_count

            metrics = {
                "train/loss": loss,
                "train/num_sequences": sequence_count,
                "train/num_tokens": token_count,
            }

            if log_to_dreadnode:
                span = TaskSpan.current()
                if span is not None:
                    TrainingStepCompleted(step=current_step, metrics=metrics).emit(span)

            # Notify callbacks
            for callback in self.callbacks:
                callback.on_step_end(current_step, self.state, metrics)

        return {
            "losses": losses,
            "total_tokens": total_tokens,
            "total_sequences": total_sequences,
        }

    def _log_checkpoint_stats(
        self,
        task: Any,
        start_step: int,
        end_step: int,
        stats: dict[str, Any],
    ) -> None:
        """Log aggregate statistics for a checkpoint."""
        losses = stats["losses"]
        avg_loss = sum(losses) / len(losses)
        min_loss = min(losses)
        max_loss = max(losses)

        task.log_output(
            "checkpoint_stats",
            {
                "steps": f"{start_step}-{end_step}",
                "avg_loss": avg_loss,
                "min_loss": min_loss,
                "max_loss": max_loss,
                "total_sequences": stats["total_sequences"],
                "total_tokens": stats["total_tokens"],
            },
        )

    def evaluate(
        self,
        eval_data: list[types.Datum],
        step: int = 0,
        log_to_dreadnode: bool = True,
    ) -> float:
        """Run evaluation on the provided data.

        Args:
            eval_data: Evaluation data as Tinker Datum objects.
            step: Current training step (for logging).
            log_to_dreadnode: Whether to log metrics to Dreadnode.

        Returns:
            Evaluation loss.
        """
        if not eval_data:
            return float("nan")

        self._initialize()

        result = self._training_client.forward(eval_data, loss_fn="cross_entropy").result()
        loss = _compute_weighted_loss(eval_data, result.loss_fn_outputs)

        metrics = {"eval/loss": loss, "eval/num_examples": len(eval_data)}

        if log_to_dreadnode:
            from dreadnode.tracing.span import TaskSpan
            from dreadnode.training.events import EvaluationCompleted

            span = TaskSpan.current()
            if span is not None:
                EvaluationCompleted(step=step, metrics=metrics).emit(span)

        for callback in self.callbacks:
            callback.on_evaluation(self.state, metrics)

        return loss

    def save_checkpoint(self, name: str | None = None) -> str:
        """Save the current model weights as a checkpoint.

        Args:
            name: Optional checkpoint name.

        Returns:
            Path to the saved checkpoint.
        """
        self._initialize()
        checkpoint_name = name or f"sft-checkpoint-step{self.state.step}"
        return self._save_checkpoint_internal(checkpoint_name)

    def _save_checkpoint_internal(self, checkpoint_name: str) -> str:
        """Internal method to save checkpoint and log as artifact."""
        save_future = self._training_client.save_weights_for_sampler(checkpoint_name)
        save_response = save_future.result()
        checkpoint_path = save_response.path

        self.state.checkpoints.append(checkpoint_path)

        # Download and log as artifact
        try:
            rest_client = self._service_client.create_rest_client()
            archive_url_future = rest_client.get_checkpoint_archive_url_from_tinker_path(
                checkpoint_path
            )
            archive_url_response = archive_url_future.result()

            with tempfile.TemporaryDirectory() as tmpdir:
                archive_path = Path(tmpdir) / f"{checkpoint_name}.tar"
                urllib.request.urlretrieve(archive_url_response.url, archive_path)

                from dreadnode.tracing.span import TaskSpan
                from dreadnode.training.events import CheckpointSaved

                span = TaskSpan.current()
                if span is not None:
                    CheckpointSaved(path=str(archive_path)).emit(span)
        except Exception:
            pass

        # Notify callbacks
        for callback in self.callbacks:
            callback.on_checkpoint(len(self.state.checkpoints), checkpoint_path, self.state)

        return checkpoint_path

    def sample(self) -> list[dict[str, str]]:
        """Generate samples from the fine-tuned model.

        Returns:
            List of sample dictionaries with 'prompt' and 'completion' keys.
        """
        self._initialize()

        if not self.config.sample_prompt:
            return []

        samples = self._sample_internal()

        # Log samples to span
        from dreadnode.tracing.span import TaskSpan

        span = TaskSpan.current()
        if span is not None:
            for idx, sample in enumerate(samples):
                span.log_output(f"sample_{idx}", sample)

        return samples

    def _sample_internal(self) -> list[dict[str, str]]:
        """Internal sampling implementation."""
        from tinker import types

        sampling_client = self._training_client.save_weights_and_get_sampling_client(
            name="tinker-sft-sample"
        )

        prompt_tokens = self._tokenizer.encode(self.config.sample_prompt, add_special_tokens=True)
        prompt = types.ModelInput.from_ints(tokens=prompt_tokens)
        sampling_params = types.SamplingParams(
            max_tokens=self.config.max_new_tokens,
            temperature=self.config.temperature,
            stop=["\n\n"],
        )

        result = sampling_client.sample(
            prompt=prompt,
            sampling_params=sampling_params,
            num_samples=self.config.num_samples,
        ).result()

        samples = []
        for _idx, sequence in enumerate(result.sequences):
            completion = self._tokenizer.decode(sequence.tokens)
            samples.append(
                {
                    "prompt": self.config.sample_prompt,
                    "completion": completion,
                }
            )

        return samples

    def _select_batch(self, data: list[types.Datum]) -> list[types.Datum]:
        """Return the next batch via shuffle-without-replacement iteration.

        Examples are consumed in a shuffled order; once every example has been
        used, the order is reshuffled for the next epoch. This guarantees each
        example is seen exactly once per epoch (random order, full coverage)
        rather than being independently resampled each step. The final batch of
        an epoch may be smaller than ``batch_size`` (no epoch-boundary spanning).
        """
        n = len(data)
        if n == 0:
            return data
        batch_size = self.config.batch_size if self.config.batch_size > 0 else n
        batch_size = min(batch_size, n)

        if self._epoch_pos >= len(self._epoch_order):
            self._epoch_order = self._rng.permutation(n).tolist()
            self._epoch_pos = 0

        batch_indices = self._epoch_order[self._epoch_pos : self._epoch_pos + batch_size]
        self._epoch_pos += len(batch_indices)
        return [data[int(idx)] for idx in batch_indices]

    def _log_training_start(
        self,
        train_data: list[types.Datum],
        eval_data: list[types.Datum] | None,
    ) -> None:
        """Log initial training information to Dreadnode."""

        from dreadnode.tracing.span import TaskSpan
        from dreadnode.training.events import TrainingStarted

        span = TaskSpan.current()
        if span is not None:
            total_tokens = sum(d.model_input.length for d in train_data)
            TrainingStarted(
                params={
                    "base_model": self.config.base_model,
                    "learning_rate": self.config.learning_rate,
                    "batch_size": self.config.batch_size,
                    "steps": self.state.total_steps,
                    "epochs": self.config.epochs,
                    "steps_per_epoch": self._steps_per_epoch,
                    "lora_rank": self.config.lora_rank,
                    "max_sequence_length": self.config.max_sequence_length,
                    "max_train_examples": self.config.max_train_examples or -1,
                    "max_eval_examples": self.config.max_eval_examples or -1,
                },
                dataset_stats={
                    "train_examples": len(train_data),
                    "eval_examples": len(eval_data) if eval_data else 0,
                    "total_tokens": total_tokens,
                },
            ).emit(span)

    def _log_training_end(self) -> None:
        """Log final training information to Dreadnode."""
        import dreadnode as dn
        from dreadnode.tracing.span import TaskSpan
        from dreadnode.training.events import TrainingCompleted

        span = TaskSpan.current()
        if span is not None:
            TrainingCompleted(
                metrics={
                    "total_tokens_processed": self.state.total_tokens_processed,
                    "total_sequences_processed": self.state.total_sequences_processed,
                    "best_loss": self.state.best_loss,
                    "elapsed_seconds": self.state.elapsed_seconds(),
                },
            ).emit(span)

        dn.push_update()

    def add_callback(self, callback: TrainingCallback) -> None:
        """Add a training callback."""
        self.callbacks.append(callback)


def _weighted_loss_components(
    data: list[types.Datum],
    outputs: list[dict[str, Any]],
) -> tuple[float, float]:
    """Return ``(sum_negative_weighted_logprobs, sum_weights)`` for a batch.

    Exposing the running sums lets callers aggregate the *exact* token-weighted
    loss across several micro-batches — which may have different sizes once the
    epoch-boundary sampler hands back a partial final batch — instead of
    averaging per-micro-batch means (which would over-weight small batches).
    """
    from tinker import types

    total_weighted_logprobs = 0.0
    total_weights = 0.0

    for datum, output in zip(data, outputs, strict=False):
        logprobs_raw = output["logprobs"]
        logprobs = (
            logprobs_raw.to_numpy()
            if isinstance(logprobs_raw, types.TensorData)
            else np.asarray(logprobs_raw)
        )

        weights_raw = datum.loss_fn_inputs["weights"]
        weights = (
            weights_raw.to_numpy()
            if isinstance(weights_raw, types.TensorData)
            else np.asarray(weights_raw)
        )

        total_weighted_logprobs += float(np.dot(logprobs, weights))
        total_weights += float(weights.sum())

    return -total_weighted_logprobs, total_weights


def _compute_weighted_loss(
    data: list[types.Datum],
    outputs: list[dict[str, Any]],
) -> float:
    """Compute weighted negative log-likelihood loss over a batch.

    Args:
        data: Training data with weights.
        outputs: Forward pass outputs with logprobs.

    Returns:
        Weighted average loss (``nan`` when the batch carries no weight).
    """
    neg_weighted_logprobs, total_weights = _weighted_loss_components(data, outputs)
    if total_weights == 0:
        return float("nan")
    return float(neg_weighted_logprobs / total_weights)


__all__ = [
    "TinkerSFTTrainer",
    "TrainingCallback",
    "TrainingState",
]
