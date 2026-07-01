"""Configuration for Tinker-based SFT training.

Tinker is a training framework for fine-tuning language models with LoRA.
This module provides configuration for supervised fine-tuning (SFT) using Tinker.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TinkerSFTConfig:
    """Configuration for Tinker-based supervised fine-tuning.

    This configuration is used to set up LoRA-based SFT training
    with the Tinker framework.

    Example:
        config = TinkerSFTConfig(
            base_model="meta-llama/Llama-3.1-8B-Instruct",
            learning_rate=1e-4,
            steps=100,
            lora_rank=16,
        )
    """

    # Model configuration
    base_model: str = "meta-llama/Llama-3.1-8B-Instruct"
    """Model name or path for the base model to fine-tune."""

    base_url: str | None = None
    """Tinker service URL. If None, uses default from environment."""

    lora_rank: int = 16
    """LoRA rank parameter for adapter training."""

    # Data configuration
    data_dir: str = "data"
    """Directory containing parquet dataset files."""

    train_split: str = "train"
    """Prefix for training data files (e.g., 'train_*.parquet')."""

    eval_split: str | None = "test"
    """Prefix for evaluation data files. Set to None to skip eval."""

    max_train_examples: int | None = None
    """Maximum number of training examples. None for all."""

    max_eval_examples: int | None = None
    """Maximum number of evaluation examples. None for all."""

    max_sequence_length: int = 2048
    """Maximum sequence length for tokenization (truncates from left)."""

    # Training configuration
    batch_size: int = 16
    """Number of sequences per training step."""

    gradient_accumulation_steps: int = 1
    """Number of micro-batches to accumulate before each optimizer step."""

    learning_rate: float = 1e-4
    """Adam optimizer learning rate."""

    steps: int | None = None
    """Maximum number of optimizer steps (a compute budget).

    When ``epochs`` is also set, training stops at whichever limit is reached
    first (``min``), and a warning is emitted if this cap cuts an epoch short.
    When both ``steps`` and ``epochs`` are ``None``, training defaults to a
    single epoch (one full pass over the data)."""

    epochs: int | None = None
    """Number of passes over the training data — the primary training-length
    knob. Each epoch runs ``ceil(num_examples / effective_batch_size)``
    optimizer steps, where ``effective_batch_size = batch_size *
    gradient_accumulation_steps``."""

    checkpoint_interval: int = 10
    """Save checkpoint every N training steps."""

    # Adam optimizer parameters
    adam_beta1: float = 0.9
    """Adam beta1 parameter."""

    adam_beta2: float = 0.95
    """Adam beta2 parameter."""

    adam_eps: float = 1e-8
    """Adam epsilon parameter."""

    # Sampling/generation configuration
    sample_prompt: str = ""
    """Prompt used for sampling after training."""

    max_new_tokens: int = 64
    """Maximum new tokens when sampling."""

    temperature: float = 0.0
    """Sampling temperature (0.0 for greedy)."""

    num_samples: int = 4
    """Number of samples to generate after training."""

    skip_sample: bool = False
    """Skip sampling after training checkpoints."""

    # Dreadnode integration
    project: str | None = None
    """Dreadnode project name for logging."""

    run_name: str | None = None
    """Dreadnode run name."""

    tags: list[str] = field(default_factory=lambda: ["training", "sft", "tinker"])
    """Tags for the Dreadnode run."""

    # Random seed
    seed: int = 0
    """Random seed for batch selection."""

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if self.lora_rank <= 0:
            raise ValueError("lora_rank must be positive")
        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")
        if self.gradient_accumulation_steps <= 0:
            raise ValueError("gradient_accumulation_steps must be positive")
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be positive")
        if self.steps is not None and self.steps <= 0:
            raise ValueError("steps must be positive")
        if self.epochs is not None and self.epochs <= 0:
            raise ValueError("epochs must be positive")
        if self.checkpoint_interval <= 0:
            raise ValueError("checkpoint_interval must be positive")


__all__ = ["TinkerSFTConfig"]
