"""Policy configuration dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field

from .defaults import (
    DEFAULT_BLOCKED_AFTER_MINUTES,
    DEFAULT_CONFIDENCE_MINIMUM,
    DEFAULT_COVERAGE_THRESHOLD,
    DEFAULT_ESCALATION_TRIGGERS,
    DEFAULT_MAX_HIGH_SEVERITY,
    DEFAULT_MAX_MEDIUM_SEVERITY,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MAX_WALL_CLOCK_MINUTES,
    DEFAULT_RETRY_BUDGET,
)


@dataclass(frozen=True)
class PRReviewPolicy:
    """Configuration for PR review approval decisions.

    Attributes:
        max_high_severity: Maximum high-severity findings allowed (0 = any blocks).
        max_medium_severity: Maximum medium-severity findings allowed.
        confidence_minimum: Minimum confidence for autonomous decision.
        escalation_triggers: Patterns that trigger escalation to human review.
    """

    max_high_severity: int = DEFAULT_MAX_HIGH_SEVERITY
    max_medium_severity: int = DEFAULT_MAX_MEDIUM_SEVERITY
    confidence_minimum: float = DEFAULT_CONFIDENCE_MINIMUM
    escalation_triggers: tuple[str, ...] = field(default_factory=lambda: DEFAULT_ESCALATION_TRIGGERS)


@dataclass(frozen=True)
class WorkOnIssuePolicy:
    """Configuration for work-on-issue workflow decisions.

    Attributes:
        retry_budget: Maximum retry attempts before stopping (workflow-level default).
        blocked_after_minutes: Minutes without progress before declaring blocked.
        coverage_threshold: Minimum test coverage percentage.
        node_retry_budgets: Per-node retry budget overrides. Maps node name to
            max retries for that node. Absent nodes fall back to ``retry_budget``.
    """

    retry_budget: int = DEFAULT_RETRY_BUDGET
    blocked_after_minutes: int = DEFAULT_BLOCKED_AFTER_MINUTES
    coverage_threshold: int = DEFAULT_COVERAGE_THRESHOLD
    node_retry_budgets: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class SharedBudgetPolicy:
    """Configuration for shared budget enforcement across workflows.

    Attributes:
        max_tokens: Maximum token consumption before halting.
        max_wall_clock_minutes: Maximum wall-clock minutes before halting.
    """

    max_tokens: int = DEFAULT_MAX_TOKENS
    max_wall_clock_minutes: int = DEFAULT_MAX_WALL_CLOCK_MINUTES


@dataclass(frozen=True)
class PolicyConfig:
    """Top-level policy configuration container.

    Attributes:
        pr_review: PR review policy settings.
        work_on_issue: Work-on-issue policy settings.
        shared: Shared budget policy settings.
    """

    pr_review: PRReviewPolicy = field(default_factory=PRReviewPolicy)
    work_on_issue: WorkOnIssuePolicy = field(default_factory=WorkOnIssuePolicy)
    shared: SharedBudgetPolicy = field(default_factory=SharedBudgetPolicy)
