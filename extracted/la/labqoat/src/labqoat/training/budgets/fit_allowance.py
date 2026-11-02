"""Immutable scientific allowance validation shared by function and class declarations."""

from dataclasses import dataclass


@dataclass(frozen=True)
class FitAllowance:
    """Declare cumulative fit milliseconds independently of execution and queue timeouts."""

    milliseconds: int

    def __post_init__(self) -> None:
        """Require an exact positive allowance representable by every JSON client."""
        if type(self.milliseconds) is not int or not 1 <= self.milliseconds <= 9_007_199_254_740_991:
            raise ValueError("Fit allowance must be a positive portable integer in milliseconds")

    def validate_isolation(self, workers: object) -> int:
        """Shared mutable workers cannot be safely terminated for a single scientific fit."""
        if workers is not None:
            raise ValueError("Fit budgets require isolated execution without reusable workers")
        return self.milliseconds
