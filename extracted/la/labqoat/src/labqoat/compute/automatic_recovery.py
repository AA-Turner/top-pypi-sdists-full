"""Explicit retained restart/resume policy for automatic replacements in one execution cycle."""

from dataclasses import dataclass
from typing import Literal

from labqoat._generated.automatic_recovery_policy import AutomaticRecoveryPolicy


@dataclass(frozen=True)
class AutomaticRecovery:
    """Keep resume fallback opt-in and bound failure repetition, admission delay and cycle lifetime."""

    strategy: Literal["restart", "resume"] = "resume"
    restart_fallback: bool = False
    failure_classes: tuple[Literal["infrastructure", "application", "publication"], ...] = ("infrastructure",)
    backoff_ms: int = 1000
    max_backoff_ms: int = 60000
    jitter_percent: int = 20
    deadline_seconds: int = 86400
    repeated_failure_limit: int = 3

    def capture(self) -> AutomaticRecoveryPolicy:
        """Validate bounded policy before publication; Function.retries remains the replacement cap."""
        self.validate()
        return AutomaticRecoveryPolicy(
            strategy=self.strategy,
            restart_fallback=self.restart_fallback,
            failure_classes=list(self.failure_classes),
            backoff_ms=self.backoff_ms,
            max_backoff_ms=self.max_backoff_ms,
            jitter_percent=self.jitter_percent,
            deadline_seconds=self.deadline_seconds,
            repeated_failure_limit=self.repeated_failure_limit,
        )

    def validate(self) -> None:
        """Reject invalid classes, implicit truth values and unbounded operational clocks."""
        bounds = (
            (self.backoff_ms, 0, 600000),
            (self.max_backoff_ms, 0, 3600000),
            (self.jitter_percent, 0, 100),
            (self.deadline_seconds, 1, 2592000),
            (self.repeated_failure_limit, 1, 11),
        )
        for value, minimum, maximum in bounds:
            if type(value) is not int or not minimum <= value <= maximum:
                raise ValueError("Automatic recovery policy values must be bounded integers")
        if self.backoff_ms > self.max_backoff_ms:
            raise ValueError("Automatic recovery backoff_ms cannot exceed max_backoff_ms")
        self.validate_selection()

    def validate_selection(self) -> None:
        """Retain only explicit supported selection and distinct retryable failure classes."""
        if self.strategy not in ("restart", "resume") or type(self.restart_fallback) is not bool:
            raise ValueError("Automatic recovery needs an explicit strategy and boolean restart_fallback")
        allowed = {"infrastructure", "application", "publication"}
        classes = set(self.failure_classes)
        if not classes or not classes <= allowed or len(classes) != len(self.failure_classes):
            raise ValueError("Automatic recovery failure_classes must be distinct supported classes")
