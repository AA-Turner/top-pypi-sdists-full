"""Workflow execution context for policy evaluators."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class WorkflowContext:
    """Captures the current state of workflow execution for policy evaluation.

    Attributes:
        tokens_consumed: Total tokens consumed so far (None if not tracked).
        elapsed_minutes: Total wall-clock minutes elapsed.
        retry_counts: Map of operation name to current retry count.
        step_history: List of timestamped step entries used for progress
            detection. Entries may include keys such as 'step' (str) and
            'entered_at' (typically an ISO-8601 str), but evaluators must
            tolerate keys being absent or values being non-string.
        recent_outcomes: List of recent outcome strings for pattern detection.
    """

    tokens_consumed: int | None = None
    elapsed_minutes: float = 0.0
    retry_counts: dict[str, int] = field(default_factory=dict)
    step_history: list[dict[str, object]] = field(default_factory=list)
    recent_outcomes: list[str] = field(default_factory=list)
