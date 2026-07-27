"""Item #7 — Tool-budget per turn."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

__all__ = ["ToolBudget", "BudgetDecision"]


@dataclass
class BudgetDecision:
    allowed: bool
    reason: str = ""


@dataclass
class ToolBudget:
    max_calls: int = 12
    _used: int = 0
    _by_kind: Counter = field(default_factory=Counter)

    def allow(self, tool_kind: str) -> BudgetDecision:
        if self._used >= self.max_calls:
            return BudgetDecision(
                allowed=False,
                reason=f"tool budget exceeded ({self._used}/{self.max_calls})",
            )
        self._used += 1
        self._by_kind[tool_kind] += 1
        return BudgetDecision(allowed=True)

    def start_new_turn(self) -> None:
        self._used = 0
        self._by_kind.clear()

    def summary(self) -> dict[str, int]:
        return dict(self._by_kind)
