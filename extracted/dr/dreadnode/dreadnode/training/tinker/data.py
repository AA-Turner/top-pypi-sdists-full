"""Data loading and preprocessing utilities for Tinker SFT training.

This module provides utilities for loading and converting datasets into the
Datum format required by Tinker for supervised fine-tuning.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

import numpy as np

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

    from tinker import types

    from dreadnode.training.etl.worlds import OpenAIConversation
    from dreadnode.training.tinker.renderer import Renderer, TrainOnWhat

    from .config import TinkerSFTConfig


@dataclass
class TinkerDataset:
    """Container for train and eval datasets in Tinker Datum format."""

    train: list[types.Datum]
    """Training data as Tinker Datum objects."""

    eval: list[types.Datum]
    """Evaluation data as Tinker Datum objects."""


def load_dataset(
    config: TinkerSFTConfig,
    tokenizer: Any,
) -> TinkerDataset:
    """Load dataset from parquet files or fall back to default examples.

    Args:
        config: Tinker SFT configuration with data paths.
        tokenizer: Tokenizer for encoding text.

    Returns:
        TinkerDataset with train and eval splits.
    """
    loader = _ParquetDatasetLoader(config, tokenizer)
    dataset = loader.try_load()
    if dataset:
        return dataset

    datums = [convert_example_to_datum(example, tokenizer) for example in build_default_examples()]
    return TinkerDataset(train=datums, eval=[])


def load_from_messages(
    messages_list: Sequence[list[dict[str, str]]],
    tokenizer: Any,
    max_sequence_length: int | None = None,
) -> list[types.Datum]:
    """Convert a list of conversation messages to Tinker Datum objects.

    Args:
        messages_list: List of conversations, each being a list of message dicts.
        tokenizer: Tokenizer for encoding.
        max_sequence_length: Optional maximum sequence length.

    Returns:
        List of Tinker Datum objects.
    """
    return [
        convert_messages_to_datum(messages, tokenizer, max_sequence_length)
        for messages in messages_list
    ]


def load_from_examples(
    examples: Sequence[tuple[str, str]],
    tokenizer: Any,
) -> list[types.Datum]:
    """Convert a list of (input, output) pairs to Tinker Datum objects.

    Args:
        examples: List of (input, output) tuples.
        tokenizer: Tokenizer for encoding.

    Returns:
        List of Tinker Datum objects.
    """
    return [convert_example_to_datum(example, tokenizer) for example in examples]


def build_default_examples() -> list[tuple[str, str]]:
    """Return a small set of default examples for testing.

    Returns:
        List of (input, output) tuples for simple instruction following.
    """
    return [
        ("What is 2+2?", "4"),
        ("What is the capital of France?", "Paris"),
        ("Say hello", "Hello!"),
        ("Count to 3", "1, 2, 3"),
        ("What color is the sky?", "Blue"),
    ]


def convert_example_to_datum(
    example: tuple[str, str],
    tokenizer: Any,
) -> types.Datum:
    """Convert an (input, output) example to a Tinker Datum.

    Creates a Datum with weights set to:
    - 0 for prompt tokens (not used in loss)
    - 1 for completion tokens (used in loss)

    Args:
        example: Tuple of (input_text, output_text).
        tokenizer: Tokenizer for encoding.

    Returns:
        Tinker Datum object ready for training.
    """
    from tinker import types

    input_text, output_text = example
    prompt = f"Input: {input_text}\nOutput:"

    prompt_tokens = tokenizer.encode(prompt, add_special_tokens=True)
    prompt_weights = [0] * len(prompt_tokens)

    completion = f" {output_text}\n"
    completion_tokens = tokenizer.encode(completion, add_special_tokens=False)
    completion_weights = [1] * len(completion_tokens)

    tokens = prompt_tokens + completion_tokens
    weights = prompt_weights + completion_weights

    # Shift for autoregressive training
    input_tokens = tokens[:-1]
    target_tokens = tokens[1:]
    target_weights = weights[1:]

    return types.Datum(
        model_input=types.ModelInput.from_ints(tokens=input_tokens),
        loss_fn_inputs={
            "target_tokens": np.asarray(target_tokens, dtype=np.int32),
            "weights": np.asarray(target_weights, dtype=np.float32),
        },
    )


def convert_messages_to_datum(
    messages: list[dict[str, str]],
    tokenizer: Any,
    max_length: int | None = None,
) -> types.Datum:
    """Convert a list of chat messages to a Tinker Datum.

    Creates a Datum with weights set to:
    - 0 for system/user tokens
    - 1 for assistant tokens (used in loss)

    Args:
        messages: List of message dicts with 'role' and 'content' keys.
        tokenizer: Tokenizer for encoding.
        max_length: Optional maximum sequence length (truncates from left).

    Returns:
        Tinker Datum object ready for training.
    """
    from tinker import types

    tokens: list[int] = []
    weights: list[float] = []
    first_segment = True

    for message in messages:
        role = _normalize_role(message.get("role"))
        header_tokens = tokenizer.encode(
            f"{role.capitalize()}:\n", add_special_tokens=first_segment
        )
        first_segment = False
        tokens.extend(header_tokens)
        weights.extend([0.0] * len(header_tokens))

        content = _normalize_content(message.get("content")).strip()
        body_tokens = tokenizer.encode(
            f"{content}\n" if content else "\n", add_special_tokens=False
        )
        tokens.extend(body_tokens)
        # Only assistant tokens get weight 1 for loss computation
        weights.extend([1.0 if role == "assistant" else 0.0] * len(body_tokens))

    if len(tokens) < 2:
        raise ValueError("Conversation did not produce enough tokens for training.")

    # Shift for autoregressive training
    input_tokens = tokens[:-1]
    target_tokens = tokens[1:]
    target_weights = weights[1:]

    # Truncate from left if needed
    if max_length and 0 < max_length < len(input_tokens):
        start = len(input_tokens) - max_length
        input_tokens = input_tokens[start:]
        target_tokens = target_tokens[start:]
        target_weights = target_weights[start:]

    return types.Datum(
        model_input=types.ModelInput.from_ints(tokens=input_tokens),
        loss_fn_inputs={
            "target_tokens": np.asarray(target_tokens, dtype=np.int32),
            "weights": np.asarray(target_weights, dtype=np.float32),
        },
    )


def load_from_conversations(
    conversations: Sequence[OpenAIConversation],
    renderer: Renderer,
    max_sequence_length: int | None = None,
    train_on_what: TrainOnWhat | None = None,
) -> list[types.Datum]:
    """Convert OpenAI conversations to Tinker Datum objects using a renderer.

    Args:
        conversations: List of OpenAI conversations with messages and tools.
        renderer: Model-specific renderer for tokenization.
        max_sequence_length: Optional maximum sequence length.
        train_on_what: Which assistant messages to train on.

    Returns:
        List of Tinker Datum objects.
    """
    from dreadnode.training.tinker.renderer import TrainOnWhat

    if train_on_what is None:
        train_on_what = TrainOnWhat.ALL_ASSISTANT_MESSAGES
    return [
        conversation_to_datum(
            conv["messages"],
            conv.get("tools"),
            renderer,
            max_sequence_length,
            train_on_what,
        )
        for conv in conversations
    ]


def conversation_to_datum(
    messages: list[Any],
    tools: list[Any] | None,
    renderer: Renderer,
    max_length: int | None,
    train_on_what: TrainOnWhat,
) -> types.Datum:
    """Convert a single conversation into a Tinker Datum via a renderer.

    Args:
        messages: List of OpenAI message dicts.
        tools: Optional list of tool schemas.
        renderer: Model-specific renderer.
        max_length: Optional max sequence length (truncates from left).
        train_on_what: Which assistant messages to train on.

    Returns:
        Tinker Datum object ready for training.
    """
    tokens, weights = renderer.build_supervised_example(messages, tools, train_on_what)
    return datum_from_tokens_and_weights(tokens, weights, max_length)


def datum_from_tokens_and_weights(
    tokens: list[int],
    weights: list[float],
    max_length: int | None = None,
) -> types.Datum:
    """Build a Tinker Datum from raw tokens and weights.

    Handles autoregressive shift and optional left-truncation.

    Args:
        tokens: Full token sequence.
        weights: Per-token loss weights (1.0 for supervised, 0.0 to mask).
        max_length: Optional max sequence length.

    Returns:
        Tinker Datum object.
    """
    from tinker import types

    if len(tokens) < 2:
        raise ValueError("Conversation did not produce enough tokens for training.")

    input_tokens = tokens[:-1]
    target_tokens = tokens[1:]
    target_weights = weights[1:]

    if max_length and 0 < max_length < len(input_tokens):
        start = len(input_tokens) - max_length
        input_tokens = input_tokens[start:]
        target_tokens = target_tokens[start:]
        target_weights = target_weights[start:]

    return types.Datum(
        model_input=types.ModelInput.from_ints(tokens=input_tokens),
        loss_fn_inputs={
            "target_tokens": np.asarray(target_tokens, dtype=np.int32),
            "weights": np.asarray(target_weights, dtype=np.float32),
        },
    )


def preview_datum(
    datum: types.Datum,
    tokenizer: Any,
    limit: int = 12,
) -> None:
    """Print a readable preview of a Tinker Datum.

    Args:
        datum: Tinker Datum to preview.
        tokenizer: Tokenizer for decoding.
        limit: Maximum number of tokens to display.
    """

    input_tokens = datum.model_input.to_ints()
    target_tokens = datum.loss_fn_inputs["target_tokens"].tolist()
    weights = datum.loss_fn_inputs["weights"].tolist()

    for idx, (inp, tgt, _wgt) in enumerate(zip(input_tokens, target_tokens, weights, strict=False)):
        if limit and idx >= limit:
            break
        tokenizer.decode([inp]).replace("\n", "\\n")
        tokenizer.decode([tgt]).replace("\n", "\\n")


class _ParquetDatasetLoader:
    """Internal loader for parquet-based datasets."""

    def __init__(self, config: TinkerSFTConfig, tokenizer: Any) -> None:
        self._config = config
        self._tokenizer = tokenizer

    def try_load(self) -> TinkerDataset | None:
        """Attempt to load train and eval datasets from parquet files."""
        data_dir = Path(self._config.data_dir)
        if not data_dir.exists():
            return None

        try:
            train_messages = self._load_split(
                data_dir,
                self._config.train_split,
                self._config.max_train_examples,
            )
        except FileNotFoundError:
            return None

        train_datums = [
            convert_messages_to_datum(messages, self._tokenizer, self._config.max_sequence_length)
            for messages in train_messages
        ]

        eval_datums: list[types.Datum] = []
        if self._config.eval_split:
            try:
                eval_messages = self._load_split(
                    data_dir,
                    self._config.eval_split,
                    self._config.max_eval_examples,
                )
                eval_datums = [
                    convert_messages_to_datum(
                        messages, self._tokenizer, self._config.max_sequence_length
                    )
                    for messages in eval_messages
                ]
            except FileNotFoundError:
                pass

        return TinkerDataset(train=train_datums, eval=eval_datums)

    def _load_split(
        self,
        data_dir: Path,
        split: str,
        limit: int | None,
    ) -> list[list[dict[str, str]]]:
        """Load a specific split from parquet files."""
        import pyarrow as pa
        import pyarrow.parquet as pq

        pattern = f"{split}_*.parquet"
        files = sorted(data_dir.glob(pattern))
        if not files:
            raise FileNotFoundError(f"No parquet files found for split '{split}' in {data_dir}")

        tables = [pq.read_table(file) for file in files]
        table = tables[0] if len(tables) == 1 else pa.concat_tables(tables, promote=True)
        table = table.combine_chunks()
        records = table.to_pylist()

        if limit is not None and limit > 0:
            records = records[:limit]

        conversations: list[list[dict[str, str]]] = []
        for record in records:
            if not isinstance(record, dict):
                continue
            normalized = _normalize_messages(record.get("messages"))
            if normalized:
                conversations.append(normalized)

        return conversations


def _normalize_messages(messages: Iterable[Any] | None) -> list[dict[str, str]]:
    """Normalize a list of message dicts."""
    normalized: list[dict[str, str]] = []
    if not messages:
        return normalized

    for message in messages:
        if not isinstance(message, dict):
            continue
        normalized.append(
            {
                "role": _normalize_role(message.get("role")),
                "content": _normalize_content(message.get("content")).strip(),
            }
        )

    return normalized


def _normalize_role(role: Any) -> str:
    """Normalize role names to standard format."""
    mapping = {
        "user": "user",
        "human": "user",
        "assistant": "assistant",
        "ai": "assistant",
        "model": "assistant",
        "system": "system",
    }
    key = (role or "").strip().lower()
    return mapping.get(key, "user")


def _normalize_content(content: Any) -> str:
    """Normalize message content to string."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        pieces: list[str] = []
        for part in content:
            if isinstance(part, dict):
                text = part.get("text")
                if isinstance(text, str):
                    pieces.append(text)
            elif isinstance(part, str):
                pieces.append(part)
        return "\n".join(pieces)
    return str(content)


__all__ = [
    "TinkerDataset",
    "build_default_examples",
    "conversation_to_datum",
    "convert_example_to_datum",
    "convert_messages_to_datum",
    "datum_from_tokens_and_weights",
    "load_dataset",
    "load_from_conversations",
    "load_from_examples",
    "load_from_messages",
    "preview_datum",
]
