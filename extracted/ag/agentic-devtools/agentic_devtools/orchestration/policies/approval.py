"""PR review approval evaluator."""

from __future__ import annotations

import math
from typing import Any

from .config import PolicyConfig
from .types import ApprovalDecision, DecisionResult


def ApprovalEvaluator(
    findings: list[dict[str, Any]],
    confidence: float,
    policy: PolicyConfig,
) -> DecisionResult[ApprovalDecision]:
    """Evaluate whether a PR should be approved, request changes, or escalate.

    Evaluation order:
    1. Check findings against escalation triggers (case-insensitive substring match)
    2. Check confidence against minimum threshold
    3. Count findings by severity and compare against thresholds

    Args:
        findings: List of finding dicts, each with at minimum a 'severity' key
            (one of 'critical', 'high', 'medium', 'low') and a 'description' key.
        confidence: PR-level confidence score (0.0 to 1.0).
        policy: Loaded policy configuration.

    Returns:
        DecisionResult with ApprovalDecision enum value and rationale.
    """
    pr_policy = policy.pr_review

    # Step 1: Escalation trigger check
    if pr_policy.escalation_triggers:
        matched_triggers: list[str] = []
        for finding in findings:
            raw_description = finding.get("description", "")
            description = "" if raw_description is None else str(raw_description).lower()
            for trigger in pr_policy.escalation_triggers:
                if trigger.lower() in description:
                    if trigger not in matched_triggers:
                        matched_triggers.append(trigger)
        if matched_triggers:
            triggers_str = ", ".join(f'"{t}"' for t in matched_triggers)
            rationale = (
                f"Escalation triggered: matched pattern(s) {triggers_str} in review findings. Human review required."
            )
            if len(rationale) > 500:
                rationale = rationale[:497] + "..."
            return DecisionResult(
                decision=ApprovalDecision.escalate,
                rationale=rationale,
                metadata={"matched_triggers": tuple(matched_triggers)},
            )

    # Step 2: Confidence check
    if not math.isfinite(confidence) or not (0.0 <= confidence <= 1.0):
        rationale = (
            f"Confidence value {confidence!r} is not a valid score "
            f"(must be a finite number in 0.0–1.0). Escalating to human review."
        )
        return DecisionResult(
            decision=ApprovalDecision.escalate,
            rationale=rationale,
            metadata={"confidence": str(confidence), "minimum": pr_policy.confidence_minimum},
        )
    if confidence < pr_policy.confidence_minimum:
        rationale = (
            f"Confidence {confidence} is below the minimum {pr_policy.confidence_minimum} "
            f"required for autonomous judgment. Escalating to human review."
        )
        return DecisionResult(
            decision=ApprovalDecision.escalate,
            rationale=rationale,
            metadata={"confidence": confidence, "minimum": pr_policy.confidence_minimum},
        )

    # Step 3: Severity threshold check
    high_count = sum(1 for f in findings if str(f.get("severity", "")).lower() in {"critical", "high"})
    medium_count = sum(1 for f in findings if str(f.get("severity", "")).lower() == "medium")
    low_count = sum(1 for f in findings if str(f.get("severity", "")).lower() == "low")

    if high_count > pr_policy.max_high_severity:
        rationale = (
            f"Found {high_count} high-severity finding(s), exceeding threshold of "
            f"{pr_policy.max_high_severity}. Requesting changes."
        )
        return DecisionResult(
            decision=ApprovalDecision.request_changes,
            rationale=rationale,
            metadata={"high_count": high_count, "medium_count": medium_count, "low_count": low_count},
        )

    if medium_count > pr_policy.max_medium_severity:
        rationale = (
            f"Found {medium_count} medium-severity finding(s), exceeding threshold of "
            f"{pr_policy.max_medium_severity}. Requesting changes."
        )
        return DecisionResult(
            decision=ApprovalDecision.request_changes,
            rationale=rationale,
            metadata={"high_count": high_count, "medium_count": medium_count, "low_count": low_count},
        )

    # All thresholds satisfied
    rationale = (
        f"All thresholds satisfied: {high_count} high "
        f"(max {pr_policy.max_high_severity}), {medium_count} medium "
        f"(max {pr_policy.max_medium_severity}). Approving."
    )
    return DecisionResult(
        decision=ApprovalDecision.approve,
        rationale=rationale,
        metadata={"high_count": high_count, "medium_count": medium_count, "low_count": low_count},
    )
