"""Per-call and aggregate usage tracking."""

from __future__ import annotations

import threading
from dataclasses import dataclass

from agentic_devtools.orchestration.llm.types import TokenUsage


@dataclass
class AggregateUsage:
    """Aggregate token usage across a workflow execution."""

    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_tokens: int = 0
    total_calls: int = 0
    total_cost_usd: float = 0.0

    def add(self, usage: TokenUsage) -> None:
        """Add a single call's usage to the aggregate."""
        self.total_input_tokens += usage.input_tokens
        self.total_output_tokens += usage.output_tokens
        self.total_tokens += usage.total_tokens
        self.total_calls += 1
        if usage.estimated_cost_usd is not None:
            self.total_cost_usd += usage.estimated_cost_usd


class UsageTracker:
    """Thread-safe usage tracker for LLM calls within a workflow.

    Tracks per-call and aggregate token usage using a threading lock
    for safe concurrent access from parallel LangGraph nodes.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._aggregate = AggregateUsage()
        self._calls: list[TokenUsage] = []

    @property
    def aggregate(self) -> AggregateUsage:
        """Return current aggregate usage (snapshot)."""
        with self._lock:
            return AggregateUsage(
                total_input_tokens=self._aggregate.total_input_tokens,
                total_output_tokens=self._aggregate.total_output_tokens,
                total_tokens=self._aggregate.total_tokens,
                total_calls=self._aggregate.total_calls,
                total_cost_usd=self._aggregate.total_cost_usd,
            )

    @property
    def calls(self) -> list[TokenUsage]:
        """Return list of per-call usage records."""
        with self._lock:
            return list(self._calls)

    def record(self, usage: TokenUsage | None) -> None:
        """Record a single call's usage.

        Args:
            usage: Token usage from an LLM response. If None, records
                   a zero-fill entry (provider didn't supply usage).
        """
        if usage is None:
            usage = TokenUsage(input_tokens=0, output_tokens=0, total_tokens=0)

        with self._lock:
            self._calls.append(usage)
            self._aggregate.add(usage)

    def reset(self) -> None:
        """Reset all tracked usage."""
        with self._lock:
            self._aggregate = AggregateUsage()
            self._calls.clear()
