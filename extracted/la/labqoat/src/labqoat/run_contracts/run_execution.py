"""Bounded finite workload execution declarations."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class RunExecution:
    """Parallelism, completion, retry, and deadline requirements."""

    parallelism: int
    completions: int
    timeout_seconds: int
    max_attempts: int
    indexed: bool = True

    def __post_init__(self) -> None:
        """Reject contradictory or unbounded execution requests."""
        if self.parallelism <= 0 or self.completions <= 0:
            raise ValueError("Parallelism and completions must be positive")
        if self.parallelism > self.completions:
            raise ValueError("Parallelism cannot exceed completions")
        if self.timeout_seconds <= 0 or self.max_attempts <= 0:
            raise ValueError("Timeout and attempts must be positive")
        if not self.indexed and self.completions != 1:
            raise ValueError("Nonindexed runs require one completion")
