"""Result models for the SDK review gate.

Kept in a leaf module (stdlib-only imports) so consumers that only need the
result types — e.g. ``plato.workflows.structured``'s schema review_fn — can
import them without pulling in :mod:`plato.agents.review_gate`, whose
``AgentTask`` import would otherwise close an import cycle
(``plato.agents.task`` → ``plato.cli`` → ``plato.workflows`` →
``review_gate`` → ``plato.agents.task``). :mod:`plato.agents.review_gate`
re-exports both names, so existing imports keep working.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

__all__ = ["ReviewGateResult", "ReviewGateMergeResult"]


@dataclass
class ReviewGateResult:
    """Result from a review function.

    Attributes:
        passed: Whether the review passed (agent work is acceptable).
        feedback: Human-readable feedback for the agent on failure.
        result_data: Arbitrary JSON-serializable dict with full review details.
            Attached to the OTel span as ``plato.review.result_json``.
        score: Optional numeric score (0.0-1.0).
        verdict: Optional verdict string (e.g. "pass", "fail").
        failure_kind: Optional machine-readable failure class.
        exhaustion_policy_override: Optional per-result override for what to do
            when review continuations are exhausted.
        continuation_cap_cost: Cost charged against the continuation budget
            for this review outcome. Use ``0.0`` for failures that should
            keep looping without consuming the PR-review cap.
    """

    passed: bool
    feedback: str = ""
    result_data: dict[str, Any] = field(default_factory=dict)
    score: float | None = None
    verdict: str | None = None
    failure_kind: str = ""
    exhaustion_policy_override: Literal["fail", "merge", "raise"] | None = None
    continuation_cap_cost: float = 1.0


@dataclass(frozen=True)
class ReviewGateMergeResult:
    """Outcome of the post-review merge attempt."""

    merged: bool
    conflict_files: list[str] = field(default_factory=list)
    error: str = ""
