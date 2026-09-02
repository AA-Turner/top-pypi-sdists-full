"""Token counting and context window management."""

from __future__ import annotations

from enum import Enum
from typing import Any, TypeVar

from agentic_devtools.orchestration.llm.errors import ContextWindowOverflowError
from agentic_devtools.orchestration.llm.types import LLMMessage

# Model to encoding mapping
MODEL_ENCODINGS: dict[str, str] = {
    "gpt-4o": "o200k_base",
    "gpt-4o-mini": "o200k_base",
    "gpt-4-turbo": "cl100k_base",
    "gpt-4": "cl100k_base",
    "gpt-3.5-turbo": "cl100k_base",
}

# Model context window sizes
MODEL_CONTEXT_WINDOWS: dict[str, int] = {
    "gpt-4o": 128000,
    "gpt-4o-mini": 128000,
    "gpt-4-turbo": 128000,
    "gpt-4": 8192,
    "gpt-3.5-turbo": 16385,
}

DEFAULT_ENCODING = "cl100k_base"
DEFAULT_CONTEXT_WINDOW = 128000

# Standard per-message token overhead constants for chat-completions format.
# Role and name fields are treated as fixed-cost metadata rather than tokenized
# strings to prevent overcounting when non-standard role values are used.
_TOKENS_PER_MESSAGE = 4  # per-message overhead (start token, role separator, end tokens)
_TOKENS_PER_NAME = 1  # additional overhead when the 'name' field is present

_VT = TypeVar("_VT")


def _prefix_lookup(table: dict[str, _VT], model: str, default: _VT) -> _VT:
    """Resolve *model* against *table* via exact match then longest-prefix match.

    Falls back to *default* when no entry matches.  Longest prefix wins so that a
    versioned model ID such as ``gpt-4o-2024-05-13`` is mapped to ``gpt-4o`` rather
    than the shorter ``gpt-4`` prefix (mirrors the strategy used by
    :class:`~agentic_devtools.orchestration.llm.cost_estimator.PricingTable`).
    When two keys share the same length and both match, the winner is determined by
    the iteration order of *table* after sorting by descending key length (i.e.
    undefined among equal-length matches, but equal-length model name collisions are
    not expected in practice).
    """
    if model in table:
        return table[model]
    for key in sorted(table, key=len, reverse=True):
        if model.startswith(key):
            return table[key]
    return default


class TruncationStrategy(str, Enum):
    """Strategy for handling context window overflow."""

    NONE = "none"  # Raise error
    TAIL = "tail"  # Keep last N tokens
    HEAD = "head"  # Keep first N tokens


class TokenCounter:
    """Model-aware token counting using tiktoken."""

    def __init__(self, model: str = "gpt-4o") -> None:
        self._model = model
        self._encoding_name = _prefix_lookup(MODEL_ENCODINGS, model, DEFAULT_ENCODING)
        self._encoding: Any = None

    def _get_encoding(self) -> Any:
        """Lazily load tiktoken encoding."""
        if self._encoding is None:
            import tiktoken

            self._encoding = tiktoken.get_encoding(self._encoding_name)
        return self._encoding

    def count_tokens(self, text: str) -> int:
        """Count tokens in a text string."""
        encoding = self._get_encoding()
        return len(encoding.encode(text))

    def count_message_tokens(self, messages: list[LLMMessage]) -> int:
        """Count total tokens across messages.

        Includes per-message overhead tokens (role, separators).
        """
        total = 0
        for msg in messages:
            total += self._count_single_message_tokens(msg)
        # Priming tokens
        total += 3
        return total

    def _count_single_message_tokens(self, msg: LLMMessage) -> int:
        """Count tokens for a single chat message using standard overhead constants.

        Role and name fields contribute fixed overhead rather than variable-length
        tokenized strings, consistent with the chat-completions token accounting
        approach and avoids overcounting with non-standard role values.
        """
        msg_tokens = _TOKENS_PER_MESSAGE + self.count_tokens(msg.content)
        if msg.name:
            msg_tokens += _TOKENS_PER_NAME
        return msg_tokens

    def check_context_window(
        self,
        messages: list[LLMMessage],
        *,
        max_output_tokens: int = 4096,
        truncation: TruncationStrategy = TruncationStrategy.NONE,
    ) -> list[LLMMessage]:
        """Check if messages fit within the model's context window.

        Args:
            messages: Messages to check.
            max_output_tokens: Reserved tokens for output.
            truncation: Strategy when overflow occurs.

        Returns:
            Messages (possibly truncated) that fit.

        Raises:
            ContextWindowOverflowError: If truncation is NONE and messages overflow.
        """
        context_window = _prefix_lookup(MODEL_CONTEXT_WINDOWS, self._model, DEFAULT_CONTEXT_WINDOW)
        if max_output_tokens < 0:
            raise ValueError(f"max_output_tokens ({max_output_tokens}) must be non-negative")
        if max_output_tokens >= context_window:
            raise ValueError(
                f"max_output_tokens ({max_output_tokens}) must be less than the context window "
                f"({context_window}) for model '{self._model}'"
            )
        available_tokens = context_window - max_output_tokens
        token_count = self.count_message_tokens(messages)

        if token_count <= available_tokens:
            return messages

        if truncation == TruncationStrategy.NONE:
            raise ContextWindowOverflowError(
                f"Input ({token_count} tokens) exceeds available context "
                f"({available_tokens} tokens) for model {self._model}",
                token_count=token_count,
                max_tokens=available_tokens,
                model=self._model,
            )

        # Apply truncation
        return self._truncate_messages(messages, available_tokens, truncation)

    def _truncate_messages(
        self,
        messages: list[LLMMessage],
        max_tokens: int,
        strategy: TruncationStrategy,
    ) -> list[LLMMessage]:
        """Truncate messages to fit within token budget.

        Applies HEAD or TAIL truncation by removing messages until the remaining
        list fits within max_tokens. Raises ContextWindowOverflowError if no
        single message fits after truncation.

        For unrecognised strategies (neither HEAD nor TAIL), the original
        messages list is returned unchanged without raising an error.
        """
        if not messages:
            return []
        if strategy == TruncationStrategy.TAIL:
            # Keep last messages that fit
            result: list[LLMMessage] = []
            total = 3  # priming tokens
            for msg in reversed(messages):
                msg_tokens = self._count_single_message_tokens(msg)
                if total + msg_tokens > max_tokens:
                    break
                result.insert(0, msg)
                total += msg_tokens
            if result:
                return result
            smallest_message_tokens = min(self._count_single_message_tokens(msg) for msg in messages)
            raise ContextWindowOverflowError(
                f"Truncation failed: no single message fits within the available token budget "
                f"({max_tokens} tokens) for model {self._model}",
                token_count=smallest_message_tokens + 3,
                max_tokens=max_tokens,
                model=self._model,
            )
        elif strategy == TruncationStrategy.HEAD:
            # Keep first messages that fit
            result = []
            total = 3
            for msg in messages:
                msg_tokens = self._count_single_message_tokens(msg)
                if total + msg_tokens > max_tokens:
                    break
                result.append(msg)
                total += msg_tokens
            if result:
                return result
            smallest_message_tokens = min(self._count_single_message_tokens(msg) for msg in messages)
            raise ContextWindowOverflowError(
                f"Truncation failed: no single message fits within the available token budget "
                f"({max_tokens} tokens) for model {self._model}",
                token_count=smallest_message_tokens + 3,
                max_tokens=max_tokens,
                model=self._model,
            )
        return messages


def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """Count tokens in a text string for the given model."""
    counter = TokenCounter(model)
    return counter.count_tokens(text)


def check_context_window(
    messages: list[LLMMessage],
    model: str = "gpt-4o",
    *,
    max_output_tokens: int = 4096,
    truncation: TruncationStrategy = TruncationStrategy.NONE,
) -> list[LLMMessage]:
    """Check if messages fit within model's context window."""
    counter = TokenCounter(model)
    return counter.check_context_window(
        messages,
        max_output_tokens=max_output_tokens,
        truncation=truncation,
    )
