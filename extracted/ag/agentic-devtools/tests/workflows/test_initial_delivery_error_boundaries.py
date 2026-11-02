"""End-to-end exception boundaries for initial-delivery recovery."""

from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.models import IssueCommentInfo, PRMetadata
from agentic_devtools.cli.ci.pipeline.actions.retry_failed_session import RetryFailedSessionAction
from agentic_devtools.cli.ci.pipeline.delivery import InitialDeliveryEvidence, InitialDeliveryOutcome
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError

RECOVERY = "agentic_devtools.cli.ci.pipeline.actions.initial_delivery_recovery"
RETRY = "agentic_devtools.cli.ci.pipeline.actions.retry_failed_session"
HEAD = "a" * 40


def _context(task_id, outcome, *, recovery_created_at=None, dispatch_error=None, label_errors=None):
    metadata = PRMetadata(
        12,
        "Task",
        "copilot/feature",
        HEAD,
        "main",
        head_repo_full_name="org/repo",
        base_repo_full_name="org/repo",
        changed_files=0,
    )
    provider = MagicMock()
    provider.get_pr_metadata.return_value = metadata
    provider.get_agent_task_prompt.return_value = "Implement the original issue"
    provider.list_closing_issues.return_value = []
    provider.get_pr_body.return_value = ""
    provider.get_dispatch_login.return_value = "workflow-bot"
    provider._dispatch_agent_retry.side_effect = dispatch_error
    provider.add_label.side_effect = label_errors
    claims = provider._get_initial_delivery_claims.return_value
    claim_state = {"created_at": recovery_created_at}

    def claim(_pr, _key, purpose, _evidence):
        if purpose != "recovery" or claim_state["created_at"]:
            return False
        claim_state["created_at"] = datetime.now(UTC).isoformat()
        return True

    claims.claim.side_effect = claim
    claims._reserve_escalation.return_value = True
    claims._transition_escalation.return_value = True
    claims.read.side_effect = lambda _pr, _key, purpose: (
        {"created_at": claim_state["created_at"]} if purpose == "recovery" and claim_state["created_at"] else None
    )
    snapshot = PRStateSnapshot(
        pr_number=12,
        head_sha=HEAD,
        head_branch="copilot/feature",
        head_repo_full_name="org/repo",
        base_repo_full_name="org/repo",
        initial_delivery=InitialDeliveryEvidence(InitialDeliveryOutcome.NO_DELIVERY, "initial-task", HEAD, HEAD),
    )
    state = SessionState(outcome, task_id=task_id)
    return provider, claims, snapshot, state, RetryFailedSessionAction(provider, retry_limit=0)


@contextmanager
def _observation_patches(state):
    with (
        patch(f"{RECOVERY}.get_latest_session_state", return_value=state),
        patch(f"{RETRY}.get_latest_session_state", return_value=state),
        patch(f"{RECOVERY}.is_copilot_session_active_via_agent_task", return_value=False),
        patch(
            f"{RECOVERY}.classify_initial_delivery_with_head",
            return_value=(HEAD, InitialDeliveryOutcome.NO_DELIVERY),
        ),
    ):
        yield


@pytest.mark.parametrize(
    ("dispatch_error", "rate_limited"),
    [
        (ProviderRateLimitError(provider="github", retry_after_seconds=30, credential_identity="dispatch"), True),
        (RetryableError("dispatch response uncertain"), False),
        (RuntimeError("provider rejected dispatch"), False),
    ],
)
def test_dispatch_failure_matrix_preserves_claim_and_never_retries_dispatch(dispatch_error, rate_limited):
    provider, claims, snapshot, state, action = _context(
        "initial-task", SessionOutcome.FINISHED, dispatch_error=dispatch_error
    )
    derived = DerivedState(snapshot)
    with _observation_patches(state):
        assert action.evaluate(snapshot, derived).decision is ActionDecision.EXECUTE
        if rate_limited:
            with pytest.raises(ProviderRateLimitError) as exc_info:
                action.execute(provider, snapshot, derived)
            assert exc_info.value.retry_after_seconds == 30
        else:
            assert action.execute(provider, snapshot, derived).decision is ActionDecision.EXECUTE
        assert action.evaluate(snapshot, derived).decision is ActionDecision.BLOCKED

    claims.claim.assert_called_once()
    provider._dispatch_agent_retry.assert_called_once()
    if rate_limited:
        provider.post_comment_as_pr_token.assert_not_called()
        provider.add_label.assert_not_called()
        claims._reserve_escalation.assert_not_called()
    else:
        provider.post_comment_as_pr_token.assert_called_once()
        provider.add_label.assert_called_once_with(12, "ai-pr-loop:agent-failed")


@pytest.mark.parametrize(
    "label_error",
    [
        ProviderRateLimitError(provider="github", retry_after_seconds=45, credential_identity="label"),
        RetryableError("label write failed"),
        RuntimeError("provider rejected label"),
    ],
)
def test_finalization_failure_retries_label_without_duplicate_notice(label_error):
    created_at = (datetime.now(UTC) - timedelta(hours=2)).isoformat()
    provider, claims, snapshot, state, action = _context(
        "recovery-task",
        SessionOutcome.FAILED,
        recovery_created_at=created_at,
        label_errors=[label_error, None],
    )
    comments = []
    provider.list_issue_comments.side_effect = lambda _pr: list(comments)
    provider.post_comment_as_pr_token.side_effect = lambda _pr, body: comments.append(
        IssueCommentInfo(len(comments) + 1, "workflow-bot", body)
    )
    derived = DerivedState(snapshot)

    with _observation_patches(state):
        assert action.evaluate(snapshot, derived).decision is ActionDecision.EXECUTE
        if isinstance(label_error, ProviderRateLimitError):
            with pytest.raises(ProviderRateLimitError) as exc_info:
                action.execute(provider, snapshot, derived)
            assert exc_info.value.retry_after_seconds == 45
        else:
            assert action.execute(provider, snapshot, derived).decision is ActionDecision.FAILED

        retry_derived = DerivedState(snapshot)
        assert action.evaluate(snapshot, retry_derived).decision is ActionDecision.EXECUTE
        assert action.execute(provider, snapshot, retry_derived).decision is ActionDecision.EXECUTE

    claims.claim.assert_not_called()
    provider.post_comment_as_pr_token.assert_called_once()
    assert provider.add_label.call_count == 2
    provider.add_label.assert_called_with(12, "ai-pr-loop:agent-failed")
    provider._dispatch_agent_retry.assert_not_called()
