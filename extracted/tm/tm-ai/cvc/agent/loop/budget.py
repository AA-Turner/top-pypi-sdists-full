"""Thread-safe iteration budget shared between parent + subagents."""
from __future__ import annotations

import threading
from dataclasses import dataclass


@dataclass
class _BudgetState:
    used: int = 0
    refunded: int = 0


class IterationBudget:
    """Shared, thread-safe iteration budget.

    Parent agent creates one. Subagents inherit the same instance so they
    share the pool. ``execute_code``-style tools that batch many calls into
    one can ``refund()`` to give back iterations.
    """

    # v2.69 — Bumped defaults so detail-heavy prompts (e.g. "analyze the
    # entire project") no longer hit the wall mid-stream. Env vars
    # CVC_PARENT_BUDGET / CVC_SUBAGENT_BUDGET override at construction time.
    DEFAULT_PARENT_MAX = 200
    DEFAULT_SUBAGENT_MAX = 150

    def __init__(self, max_iterations: int = 200):
        self._max = max(1, int(max_iterations))
        self._state = _BudgetState()
        self._lock = threading.Lock()

    @classmethod
    def for_parent(cls, max_iterations: int | None = None) -> "IterationBudget":
        return cls(max_iterations or cls.DEFAULT_PARENT_MAX)

    @classmethod
    def for_subagent(cls, max_iterations: int | None = None) -> "IterationBudget":
        return cls(max_iterations or cls.DEFAULT_SUBAGENT_MAX)

    @property
    def max_iterations(self) -> int:
        return self._max

    def remaining(self) -> int:
        with self._lock:
            return self._max - self._state.used + self._state.refunded

    def used(self) -> int:
        with self._lock:
            return self._state.used

    def consume(self, n: int = 1) -> bool:
        """Consume n iterations. Returns False if budget exhausted."""
        with self._lock:
            effective = self._state.used - self._state.refunded
            if effective + n > self._max:
                return False
            self._state.used += n
            return True

    def refund(self, n: int = 1) -> None:
        """Give back iterations (e.g. for batched execute_code calls)."""
        with self._lock:
            self._state.refunded += max(0, int(n))

    def is_exhausted(self) -> bool:
        return self.remaining() <= 0

    def reset(self) -> None:
        with self._lock:
            self._state = _BudgetState()


__all__ = ["IterationBudget"]
