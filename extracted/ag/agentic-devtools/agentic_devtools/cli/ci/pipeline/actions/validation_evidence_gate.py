"""Opt-in gate for current-head validation evidence before draft PR publication."""

from __future__ import annotations

import re

from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.session_detector import is_copilot_session_active_via_agent_task
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.pipeline.validation_evidence import (
    BLOCKER_MARKER,
    EVIDENCE_REQUIRED_LABEL,
    FOLLOWUP_KEY,
    GATE_STATE_KEY,
    RECOVERY_MARKER,
    EvidenceGateState,
    agent_replied_after,
    build_blocker_comment,
    build_recovery_request,
    find_head_evidence,
    find_marker_comment,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class ValidationEvidenceGateAction:
    """Request missing validation receipts before an opted-in draft can publish."""

    may_invalidate_snapshot = False
    runs_after_invalidation = True

    @property
    def name(self) -> str:
        return "validation_evidence_gate"

    def _result(self, decision: ActionDecision, details: str) -> ActionResult:
        return ActionResult(name=self.name, decision=decision, details=details)

    def _evaluate_missing_evidence(
        self,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
        provider: CIPlatformProvider,
        comments: list[IssueCommentInfo],
    ) -> ActionResult:
        active_session = is_copilot_session_active_via_agent_task(
            snapshot.base_repo_full_name,
            snapshot.pr_number,
            head_branch=snapshot.head_branch,
            pr_id=snapshot.pr_id,
            head_sha=snapshot.head_sha,
            provider=provider,
        )
        if active_session is not False:
            return self._result(ActionDecision.SKIP, "Copilot session active or inventory unavailable")

        recovery_comment = find_marker_comment(comments, RECOVERY_MARKER)
        if recovery_comment is None:
            derived.set(FOLLOWUP_KEY, "recovery")
            return self._result(ActionDecision.EXECUTE, "Requesting one final validation-evidence receipt")

        if find_marker_comment(comments, BLOCKER_MARKER) is not None:
            return self._result(ActionDecision.SKIP, "Validation-evidence blocker already posted")

        if agent_replied_after(comments, recovery_comment):
            derived.set(FOLLOWUP_KEY, "blocker")
            return self._result(ActionDecision.EXECUTE, "Posting a human blocker after missing evidence reply")
        return self._result(ActionDecision.SKIP, "Awaiting an evidence-author response to the recovery request")

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Evaluate current-head evidence and select at most one human follow-up."""
        derived.set(GATE_STATE_KEY, EvidenceGateState.UNKNOWN)
        if not snapshot.is_draft or not snapshot.has_changes:
            derived.set(GATE_STATE_KEY, EvidenceGateState.NOT_APPLICABLE)
            return self._result(ActionDecision.SKIP, "Validation-evidence gate applies only to changed draft PRs")

        provider = derived.get("provider")
        try:
            if EVIDENCE_REQUIRED_LABEL not in snapshot.labels and EVIDENCE_REQUIRED_LABEL not in (
                provider.list_linked_issue_labels(snapshot.pr_number)
            ):
                derived.set(GATE_STATE_KEY, EvidenceGateState.NOT_APPLICABLE)
                return self._result(ActionDecision.SKIP, "Validation-evidence label is not present")

            if re.fullmatch(r"[0-9a-fA-F]{40}", snapshot.head_sha) is None:
                return self._result(ActionDecision.SKIP, "Current PR head SHA is invalid")

            comments = provider.list_issue_comments(snapshot.pr_number)
            if find_head_evidence(comments, snapshot.head_sha) is not None:
                derived.set(GATE_STATE_KEY, EvidenceGateState.SATISFIED)
                return self._result(ActionDecision.SKIP, "Current head has validation evidence")

            derived.set(GATE_STATE_KEY, EvidenceGateState.MISSING)
            return self._evaluate_missing_evidence(snapshot, derived, provider, comments)
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            derived.set(GATE_STATE_KEY, EvidenceGateState.UNKNOWN)
            return self._result(ActionDecision.SKIP, f"Validation-evidence state unavailable: {exc}")

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Post the selected bounded follow-up without changing the PR snapshot."""
        derived.set(GATE_STATE_KEY, EvidenceGateState.MISSING)
        followup = derived.get(FOLLOWUP_KEY)
        if followup == "recovery":
            body = build_recovery_request(snapshot.head_sha)
        elif followup == "blocker":
            body = build_blocker_comment(snapshot.head_sha)
        else:
            return self._result(ActionDecision.FAILED, "Unknown validation-evidence follow-up")

        try:
            provider.post_comment(snapshot.pr_number, body)
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            return self._result(ActionDecision.FAILED, f"Could not post validation-evidence follow-up: {exc}")
        return self._result(ActionDecision.EXECUTE, "Posted validation-evidence follow-up")
