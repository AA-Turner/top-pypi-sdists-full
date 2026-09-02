"""``summarize_and_decide`` node — aggregate findings and produce verdict.

Satisfies FR-004 (status cascade) and FR-006 (autonomous decision).
Uses existing ``compute_aggregate_status()`` for status derivation and
``ReviewDecisionPolicy`` for the approve/request-changes decision.
"""

from __future__ import annotations

from typing import Any


def summarize_and_decide_node(state: dict[str, Any]) -> dict[str, Any]:
    """Aggregate file review results and apply the decision policy.

    Cascades file-level statuses to an overall PR status using
    ``compute_aggregate_status()``, then evaluates the aggregated
    findings against the configured ``ReviewDecisionPolicy``.

    Args:
        state: Current ``ReviewGraphState`` containing ``file_results``.

    Returns:
        State update dict with ``overall_decision`` and ``summary``.
    """
    from agentic_devtools.cli.azure_devops.review_state import compute_aggregate_status

    from ..decision_policy import ReviewDecisionPolicy, evaluate_decision

    file_results = state.get("file_results", [])
    config = state.get("config", {})
    upstream_errors: list[str] = state.get("errors", [])

    if not file_results:
        if upstream_errors:
            return {
                "overall_decision": "request-changes",
                "summary": (
                    f"Review pipeline encountered errors and produced no file results "
                    f"({len(upstream_errors)} error(s)); defaulting to request-changes."
                ),
            }
        return {
            "overall_decision": "approve",
            "summary": "No files to review — auto-approved.",
        }

    # Compute file-level statuses for cascade
    status_map = {
        "approve": "approved",
        "request-changes": "needs-work",
        "request-changes-with-suggestion": "needs-work",
    }

    file_statuses: list[str] = []
    for result in file_results:
        outcome = (
            result.get("outcome", "approve") if isinstance(result, dict) else getattr(result, "outcome", "approve")
        )
        file_statuses.append(status_map.get(outcome, "needs-work"))

    # FR-004: Status cascade
    overall_status = compute_aggregate_status(file_statuses)

    # Count findings by severity
    high_count = 0
    medium_count = 0
    low_count = 0

    for result in file_results:
        suggestions = result.get("suggestions", []) if isinstance(result, dict) else getattr(result, "suggestions", [])
        for suggestion in suggestions:
            severity = (
                suggestion.get("severity", "low")
                if isinstance(suggestion, dict)
                else getattr(suggestion, "severity", "low")
            )
            if severity == "high":
                high_count += 1
            elif severity == "medium":
                medium_count += 1
            else:
                low_count += 1

    # FR-006: Apply decision policy — accept both hyphenated and underscore key spellings.
    # Use key-presence check (not .get()) so that an explicit ``null`` value for
    # ``decision-policy`` takes precedence and does not fall back to ``decision_policy``,
    # matching the behaviour in ``agentic_devtools/config.py:load_review_decision_policy``.
    review_config = config.get("review", {}) if isinstance(config, dict) else {}
    if isinstance(review_config, dict):
        if "decision-policy" in review_config:
            policy_config = review_config["decision-policy"]
        elif "decision_policy" in review_config:
            policy_config = review_config["decision_policy"]
        else:
            policy_config = None
    else:
        policy_config = None
    policy = ReviewDecisionPolicy.from_config(policy_config)

    # FR-006: Apply decision policy, but conservatively force request-changes when
    # upstream errors exist.  A partial pipeline (e.g. a failed fetch or scaffold)
    # means the review is incomplete; auto-approving in that state is unsafe.
    if overall_status == "needs-work" or upstream_errors:
        decision = "request-changes"
    else:
        decision = evaluate_decision(
            policy,
            high_count,
            medium_count,
            low_count,
        )

    # Build summary
    total_files = len(file_results)
    approved_files = sum(1 for s in file_statuses if s == "approved")
    needs_work_files = total_files - approved_files

    summary_parts: list[str] = []
    summary_parts.append(f"Reviewed {total_files} file(s): {approved_files} approved, {needs_work_files} need work.")

    if high_count or medium_count or low_count:
        summary_parts.append(f"Findings: {high_count} high, {medium_count} medium, {low_count} low severity.")

    summary_parts.append(f"Decision: {decision} (overall status: {overall_status}).")

    if upstream_errors:
        summary_parts.append(
            f"Note: {len(upstream_errors)} upstream pipeline error(s) forced request-changes; review may be incomplete."
        )

    return {
        "overall_decision": decision,
        "summary": " ".join(summary_parts),
    }
