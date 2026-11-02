"""Focused approval-entry guards, before identity idempotency or review mutation."""

from __future__ import annotations

from agentic_devtools.cli.ci.approver_preflight import ApproverPreflightResult
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot


def preflight_block(preflight: ApproverPreflightResult | None) -> ActionResult | None:
    """Render only fixed capability/status evidence through the existing summary."""
    if preflight is None:
        return None
    capability = preflight.blocking_capability
    if capability is None:
        return None
    evidence = getattr(preflight, capability)
    status = f"HTTP {evidence.http_status}" if evidence.http_status is not None else "HTTP status unavailable"
    return ActionResult(
        name="approve",
        decision=ActionDecision.BLOCKED,
        preconditions={"approver_preflight": False},
        details=f"Approver preflight blocked: {capability} ({evidence.status.value}; {status})",
        capability=capability,
        http_status=evidence.http_status,
    )


def approval_entry_guard(snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult | None:
    """Check capabilities before any identity-based decision or live-HEAD guard."""
    blocked = preflight_block(snapshot.approver_preflight)
    if blocked is not None:
        return blocked
    provider = derived.get("provider")
    if provider is not None:
        live_head_sha = provider.get_pr_metadata(snapshot.pr_number).head_sha
        if live_head_sha != snapshot.head_sha:
            return ActionResult(
                "approve",
                ActionDecision.SKIP,
                {"live_head_matches_snapshot": False},
                f"PR HEAD moved from {snapshot.head_sha} to {live_head_sha}",
            )
    return None
