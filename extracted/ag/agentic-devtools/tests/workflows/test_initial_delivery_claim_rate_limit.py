"""A raw claim-write rate limit remains typed through initial recovery."""

from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.initial_delivery_claims import InitialDeliveryClaims
from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.pipeline.actions.retry_failed_session import RetryFailedSessionAction
from agentic_devtools.cli.ci.pipeline.delivery import InitialDeliveryEvidence, InitialDeliveryOutcome
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError

CLAIMS = "agentic_devtools.cli.ci.initial_delivery_claims"
RECOVERY = "agentic_devtools.cli.ci.pipeline.actions.initial_delivery_recovery"
RETRY = "agentic_devtools.cli.ci.pipeline.actions.retry_failed_session"
HEAD = "a" * 40


def test_raw_claim_rate_limit_reaches_pipeline_without_replaying_write() -> None:
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
    provider._dispatch_agent_retry.return_value = 99
    provider._get_initial_delivery_claims.return_value = InitialDeliveryClaims("org/repo")
    snapshot = PRStateSnapshot(
        pr_number=12,
        head_sha=HEAD,
        head_branch="copilot/feature",
        head_repo_full_name="org/repo",
        base_repo_full_name="org/repo",
        initial_delivery=InitialDeliveryEvidence(InitialDeliveryOutcome.NO_DELIVERY, "initial-task", HEAD, HEAD),
    )
    state = SessionState(SessionOutcome.FINISHED, task_id="initial-task")
    calls = []

    def api(_endpoint, *, method="GET", body=None):
        calls.append(method)
        if method == "GET":
            raise RuntimeError("HTTP 404")
        raise RetryableError(
            "rate limited",
            retry_after=30,
            provider="github",
            credential_identity="test-credential",
            is_rate_limit=True,
        )

    action = RetryFailedSessionAction(provider, retry_limit=0)
    derived = DerivedState(snapshot)
    with (
        patch(
            f"{RECOVERY}.classify_initial_delivery_with_head", return_value=(HEAD, InitialDeliveryOutcome.NO_DELIVERY)
        ),
        patch(f"{RECOVERY}.is_copilot_session_active_via_agent_task", return_value=False),
        patch(f"{RECOVERY}.get_latest_session_state", return_value=state),
        patch(f"{RETRY}.get_latest_session_state", return_value=state),
        patch(f"{CLAIMS}.GitHubVariableBackingStore._api", side_effect=api),
    ):
        assert action.evaluate(snapshot, derived).decision is ActionDecision.EXECUTE
        with pytest.raises(ProviderRateLimitError) as exc_info:
            action.execute(provider, snapshot, derived)

    assert calls == ["GET", "PUT"]
    assert exc_info.value.retry_after_seconds == 30
    assert exc_info.value.credential_identity == "test-credential"
    provider._dispatch_agent_retry.assert_not_called()


def test_dispatch_rate_limit_keeps_claim_consumed_without_escalation() -> None:
    metadata = PRMetadata(
        12, "Task", "copilot/feature", HEAD, "main", head_repo_full_name="org/repo", base_repo_full_name="org/repo"
    )
    provider = MagicMock()
    provider.get_pr_metadata.return_value = metadata
    provider.get_agent_task_prompt.return_value = "Implement the original issue"
    provider.list_closing_issues.return_value = []
    provider.get_pr_body.return_value = ""
    provider._dispatch_agent_retry.side_effect = ProviderRateLimitError(
        provider="github", is_rate_limit=True, retry_after_seconds=30, credential_identity="test-credential"
    )
    claims = provider._get_initial_delivery_claims.return_value
    claims.claim.return_value = True
    claims.read.side_effect = lambda _pr, _key, purpose: (
        {"created_at": datetime.now(UTC).isoformat()} if purpose == "recovery" and claims.claim.called else None
    )
    snapshot = PRStateSnapshot(
        pr_number=12,
        head_sha=HEAD,
        head_branch="copilot/feature",
        head_repo_full_name="org/repo",
        base_repo_full_name="org/repo",
        initial_delivery=InitialDeliveryEvidence(InitialDeliveryOutcome.NO_DELIVERY, "initial-task", HEAD, HEAD),
    )
    state = SessionState(SessionOutcome.FINISHED, task_id="initial-task")
    action = RetryFailedSessionAction(provider, retry_limit=0)
    derived = DerivedState(snapshot)
    with (
        patch(
            f"{RECOVERY}.classify_initial_delivery_with_head", return_value=(HEAD, InitialDeliveryOutcome.NO_DELIVERY)
        ),
        patch(f"{RECOVERY}.is_copilot_session_active_via_agent_task", return_value=False),
        patch(f"{RECOVERY}.get_latest_session_state", return_value=state),
        patch(f"{RETRY}.get_latest_session_state", return_value=state),
    ):
        assert action.evaluate(snapshot, derived).decision is ActionDecision.EXECUTE
        with pytest.raises(ProviderRateLimitError) as exc_info:
            action.execute(provider, snapshot, derived)
        assert action.evaluate(snapshot, derived).decision is ActionDecision.BLOCKED

    assert exc_info.value.retry_after_seconds == 30
    assert exc_info.value.credential_identity == "test-credential"
    claims.claim.assert_called_once()
    provider._dispatch_agent_retry.assert_called_once()
    provider.post_comment_as_pr_token.assert_not_called()
    provider.add_label.assert_not_called()
