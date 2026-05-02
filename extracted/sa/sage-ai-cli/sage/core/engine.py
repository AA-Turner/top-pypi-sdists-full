"""Conversation engine — manages message history, system prompts, and context limits."""

from __future__ import annotations

from dataclasses import dataclass

from sage.providers.base import Message

# Token estimation: ~4 characters per token (conservative estimate)
CHARS_PER_TOKEN = 4


@dataclass
class ContextStats:
    """Statistics about current context usage."""

    message_count: int
    turn_count: int
    estimated_tokens: int
    max_tokens: int
    usage_percent: float
    system_prompt_tokens: int
    history_tokens: int


class ConversationEngine:
    """Maintains multi-turn conversation state with smart context management.

    Responsibilities:
      - Store message history (system + user + assistant turns)
      - Enforce context window limits by truncating oldest messages
      - Provide the full message list for each provider call
      - Estimate token usage and report context statistics
      - Smart trimming that preserves important context markers
    """

    # Markers that indicate important context to preserve
    _IMPORTANT_MARKERS = frozenset(
        {
            "ARCHITECTURE",
            "DECISION",
            "IMPORTANT",
            "NOTE:",
            "CRITICAL",
            "TODO:",
            "FIXME:",
            "File:",
            "```",  # Code blocks
        }
    )

    def __init__(
        self,
        system_prompt: str = "",
        max_history: int = 100,  # Increased from 50 for more procedural context
        max_tokens: int = 200000,  # Increased from 128000 for comprehensive task execution
    ) -> None:
        self._system_prompt = system_prompt
        self._max_history = max_history
        self._max_tokens = max_tokens
        self._messages: list[Message] = []

    # ── Public API ──────────────────────────────────────────

    @property
    def system_prompt(self) -> str:
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, value: str) -> None:
        self._system_prompt = value

    def add_user(self, content: str) -> None:
        """Append a user message."""
        self._messages.append(Message(role="user", content=content))
        self._trim()

    def add_assistant(self, content: str) -> None:
        """Append an assistant response."""
        self._messages.append(Message(role="assistant", content=content))
        self._trim()

    def build_messages(self) -> list[Message]:
        """Return the full message list to send to a provider.

        Includes the system prompt (if set) as the first message,
        followed by conversation history.
        """
        out: list[Message] = []
        if self._system_prompt:
            out.append(Message(role="system", content=self._system_prompt))
        out.extend(self._messages)
        return out

    def clear(self) -> None:
        """Reset conversation history (keeps system prompt)."""
        self._messages.clear()

    @property
    def history(self) -> list[Message]:
        """Read-only view of conversation history (excludes system prompt)."""
        return list(self._messages)

    @property
    def turn_count(self) -> int:
        """Number of user messages in history."""
        return sum(1 for m in self._messages if m.role == "user")

    # ── Token estimation ───────────────────────────────────

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for a string (4 chars ≈ 1 token)."""
        return len(text) // CHARS_PER_TOKEN

    def estimate_message_tokens(self, msg: Message) -> int:
        """Estimate tokens for a message including role overhead."""
        # Add ~4 tokens for role/formatting overhead
        return self.estimate_tokens(msg.content) + 4

    def estimate_total_tokens(self) -> int:
        """Estimate total tokens in current context."""
        total = 0
        if self._system_prompt:
            total += self.estimate_tokens(self._system_prompt) + 4
        for msg in self._messages:
            total += self.estimate_message_tokens(msg)
        return total

    def get_context_stats(self) -> ContextStats:
        """Get current context usage statistics."""
        system_tokens = self.estimate_tokens(self._system_prompt) + 4 if self._system_prompt else 0
        history_tokens = sum(self.estimate_message_tokens(m) for m in self._messages)
        total = system_tokens + history_tokens
        usage_pct = (total / self._max_tokens * 100) if self._max_tokens > 0 else 0

        return ContextStats(
            message_count=len(self._messages),
            turn_count=self.turn_count,
            estimated_tokens=total,
            max_tokens=self._max_tokens,
            usage_percent=usage_pct,
            system_prompt_tokens=system_tokens,
            history_tokens=history_tokens,
        )

    def context_status(self) -> str:
        """Get a human-readable context status string."""
        stats = self.get_context_stats()
        return (
            f"{stats.turn_count} turns, "
            f"~{stats.estimated_tokens:,} tokens "
            f"({stats.usage_percent:.1f}% of {stats.max_tokens:,})"
        )

    # ── Smart context management ─────────────────────────────

    def _has_important_content(self, msg: Message) -> bool:
        """Check if a message contains important markers to preserve."""
        content = msg.content.upper()
        return any(marker.upper() in content for marker in self._IMPORTANT_MARKERS)

    def smart_trim(self, preserve_turns: int = 4) -> int:
        """Intelligently trim context while preserving important messages.

        Args:
            preserve_turns: Minimum number of recent turns to always keep

        Returns:
            Number of messages removed
        """
        # Keep at least preserve_turns * 2 messages (user + assistant pairs)
        min_keep = preserve_turns * 2
        if len(self._messages) <= min_keep:
            return 0

        # Find messages to potentially remove (older than preserve_turns)
        candidates = self._messages[:-min_keep] if min_keep > 0 else self._messages[:]

        # Filter out important messages
        to_remove = []
        for i, msg in enumerate(candidates):
            if not self._has_important_content(msg):
                to_remove.append(i)

        # Remove in pairs (to maintain conversation coherence)
        removed = 0
        i = 0
        while i < len(to_remove) - 1:
            # Check if consecutive indices form a pair
            if to_remove[i + 1] == to_remove[i] + 1:
                # Remove the pair (adjust for already removed)
                idx = to_remove[i] - removed
                if idx >= 0 and idx + 1 < len(self._messages):
                    self._messages.pop(idx)
                    self._messages.pop(idx)  # Same index, next element shifted
                    removed += 2
                i += 2
            else:
                i += 1

        return removed

    def compact(self, target_tokens: int | None = None) -> int:
        """Compact context to fit within token budget.

        Args:
            target_tokens: Target token count (default: 80% of max)

        Returns:
            Number of messages removed
        """
        if target_tokens is None:
            target_tokens = int(self._max_tokens * 0.8)

        total_removed = 0

        # First, try smart trimming
        while self.estimate_total_tokens() > target_tokens:
            removed = self.smart_trim(preserve_turns=4)
            if removed == 0:
                break
            total_removed += removed

        # If still over, do aggressive trimming
        while self.estimate_total_tokens() > target_tokens and len(self._messages) > 8:
            # Remove oldest pair
            self._messages.pop(0)
            self._messages.pop(0)
            total_removed += 2

        return total_removed

    # ── Internal ────────────────────────────────────────────

    def _trim(self) -> None:
        """Drop oldest messages if history exceeds the limit.

        Always keeps messages in pairs (user + assistant) to avoid
        sending orphaned turns to the model.
        """
        while len(self._messages) > self._max_history:
            # Drop from the front — remove two messages (a full turn)
            if len(self._messages) >= 2:
                self._messages.pop(0)
                self._messages.pop(0)
            else:
                self._messages.pop(0)
