"""Tinker-based training backend for supervised fine-tuning.

This module provides a training backend using the Tinker framework for
LoRA-based supervised fine-tuning (SFT) of language models.

Example:
    from dreadnode.training.tinker import train_tinker_sft

    messages = [
        [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi!"}],
    ]

    state = train_tinker_sft(
        config={"base_model": "meta-llama/Llama-3.1-8B-Instruct", "steps": 100},
        messages=messages,
    )

Requirements:
    - tinker>=0.4.1
    - pyarrow>=17.0.0 (for parquet dataset loading)
"""

from __future__ import annotations

import typing as t

from dreadnode.training.tinker.config import TinkerSFTConfig
from dreadnode.training.tinker.data import (
    TinkerDataset,
    build_default_examples,
    conversation_to_datum,
    convert_example_to_datum,
    convert_messages_to_datum,
    datum_from_tokens_and_weights,
    load_dataset,
    load_from_conversations,
    load_from_examples,
    load_from_messages,
    preview_datum,
)
from dreadnode.training.tinker.renderer import (
    GptOssRenderer,
    LlamaRenderer,
    Nemotron3Renderer,
    Qwen3Renderer,
    Renderer,
    RoleColonRenderer,
    TrainOnWhat,
    get_renderer,
)
from dreadnode.training.tinker.trainer import (
    TinkerSFTTrainer,
    TrainingCallback,
    TrainingState,
)

if t.TYPE_CHECKING:
    from collections.abc import Sequence


def train_tinker_sft(
    config: dict[str, t.Any] | None = None,
    messages: Sequence[list[dict[str, str]]] | None = None,
    examples: Sequence[tuple[str, str]] | None = None,
    data_dir: str | None = None,
    project: str | None = None,
    run_name: str | None = None,
    tags: list[str] | None = None,
    log_to_dreadnode: bool = True,
) -> TrainingState:
    """Train a model using Tinker SFT.

    This function provides a high-level interface for supervised fine-tuning
    using the Tinker framework. Data can be provided in multiple formats:
    - Conversation messages (list of message dicts)
    - Simple examples (input/output pairs)
    - Parquet files in a data directory

    Args:
        config: Training configuration dict. See TinkerSFTConfig for options.
        messages: List of conversations, each a list of message dicts
            with 'role' and 'content' keys.
        examples: List of (input, output) tuples for simple supervised learning.
        data_dir: Directory containing parquet files with training data.
        project: Dreadnode project name.
        run_name: Dreadnode run name.
        tags: Tags for the Dreadnode run.
        log_to_dreadnode: Whether to log to Dreadnode (default: True).

    Returns:
        TrainingState with training metrics and checkpoint paths.

    Raises:
        ValueError: If no data source is provided.
    """
    import dreadnode as dn

    # Build configuration
    config_dict = config or {}
    if data_dir is not None:
        config_dict["data_dir"] = data_dir
    if project is not None:
        config_dict["project"] = project
    if run_name is not None:
        config_dict["run_name"] = run_name
    if tags is not None:
        config_dict["tags"] = tags

    sft_config = TinkerSFTConfig(**config_dict)

    # Create trainer
    trainer = TinkerSFTTrainer(sft_config)

    # Load data based on what's provided
    train_data = []
    eval_data = []

    if messages is not None:
        train_data = load_from_messages(
            list(messages),
            trainer.tokenizer,
            sft_config.max_sequence_length,
        )
    elif examples is not None:
        train_data = load_from_examples(list(examples), trainer.tokenizer)
    else:
        # Load from data directory
        dataset = load_dataset(sft_config, trainer.tokenizer)
        train_data = dataset.train
        eval_data = dataset.eval

    if not train_data:
        raise ValueError("No training data. Provide messages, examples, or data_dir.")

    # Set up Dreadnode run
    dn.configure()
    run_name_final = sft_config.run_name or "tinker-sft"
    project_final = sft_config.project or "tinker-sft"
    tags_final = sft_config.tags

    if log_to_dreadnode:
        with dn.run(name=run_name_final, project=project_final, tags=tags_final):
            return trainer.train(
                train_data,
                eval_data or None,
                log_to_dreadnode=True,
            )
    else:
        return trainer.train(
            train_data,
            eval_data or None,
            log_to_dreadnode=False,
        )


__all__ = [
    # Data utilities
    "TinkerDataset",
    # Configuration
    "TinkerSFTConfig",
    # Trainer
    "TinkerSFTTrainer",
    "TrainingCallback",
    "TrainingState",
    # Renderers
    "GptOssRenderer",
    "LlamaRenderer",
    "Nemotron3Renderer",
    "Qwen3Renderer",
    "Renderer",
    "RoleColonRenderer",
    "TrainOnWhat",
    "build_default_examples",
    "conversation_to_datum",
    "convert_example_to_datum",
    "convert_messages_to_datum",
    "datum_from_tokens_and_weights",
    "get_renderer",
    "load_dataset",
    "load_from_conversations",
    "load_from_examples",
    "load_from_messages",
    "preview_datum",
    # High-level functions
    "train_tinker_sft",
]
