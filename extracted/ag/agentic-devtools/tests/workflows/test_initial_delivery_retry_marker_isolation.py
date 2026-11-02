"""Verify initial-delivery notices do not consume ordinary retry policy."""

import base64
import json
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.guards import AGENT_FAILED_LABEL
from agentic_devtools.cli.ci.initial_delivery_claims import InitialDeliveryClaims
from agentic_devtools.cli.ci.models import IssueCommentInfo, PRMetadata
from agentic_devtools.cli.ci.pipeline.actions.initial_delivery_recovery import InitialDeliveryRecovery
from agentic_devtools.cli.ci.pipeline.actions.retry_failed_session import RetryFailedSessionAction
from agentic_devtools.cli.ci.pipeline.delivery import InitialDeliveryEvidence, InitialDeliveryOutcome
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from tests.workflows.test_initial_delivery_recovery import _CreateOnlyClaimsFake, _FakeAgentTaskRest

RECOVERY = "agentic_devtools.cli.ci.pipeline.actions.initial_delivery_recovery"
RETRY = "agentic_devtools.cli.ci.pipeline.actions.retry_failed_session"
HEAD = "a" * 40
DELIVERED_HEAD = "b" * 40


def test_initial_delivery_notice_does_not_exhaust_unrelated_failed_retry(monkeypatch) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "workflow-token")
    provider = GitHubActionsProvider(repo="org/repo")
    evidence = InitialDeliveryEvidence(InitialDeliveryOutcome.NO_DELIVERY, "initial-task", HEAD, HEAD)
    snapshot = PRStateSnapshot(
        pr_number=12,
        head_sha=HEAD,
        head_branch="copilot/feature",
        head_repo_full_name="org/repo",
        base_repo_full_name="org/repo",
        initial_delivery=evidence,
    )
    metadata = [
        PRMetadata(
            12,
            "Task",
            snapshot.head_branch,
            HEAD,
            "main",
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            changed_files=0,
        )
    ]
    session = [SessionState(SessionOutcome.FAILED, task_id="recovery-task")]
    comments: list[IssueCommentInfo] = []
    claims_fake = _CreateOnlyClaimsFake(writer_on_claim=None)
    github_api = _FakeAgentTaskRest(claims_fake, snapshot.head_branch)
    recovery_key = InitialDeliveryRecovery._identity(evidence)

    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=github_api),
        patch.object(InitialDeliveryClaims, "_api", side_effect=claims_fake),
        patch.object(provider, "get_pr_metadata", side_effect=lambda *_: metadata[0]),
        patch.object(provider, "get_ref_sha", return_value="c" * 40),
        patch.object(
            provider,
            "list_pr_files_complete",
            side_effect=lambda *_: [] if metadata[0].changed_files == 0 else ["src/app.py"],
        ),
        patch.object(provider, "list_issue_comments", return_value=comments),
        patch.object(provider, "get_dispatch_login", return_value="workflow-bot"),
        patch.object(provider, "get_agent_task_prompt", return_value="Continue the original task"),
        patch.object(provider, "post_comment_as_pr_token") as post_comment,
        patch.object(
            provider,
            "add_label",
            side_effect=lambda *_: metadata.__setitem__(0, replace(metadata[0], labels=[AGENT_FAILED_LABEL])),
        ) as add_label,
        patch.object(
            provider,
            "remove_label",
            side_effect=lambda *_: metadata.__setitem__(0, replace(metadata[0], labels=[])),
        ) as remove_label,
        patch.object(provider, "dispatch_agent_retry") as dispatch,
        patch(f"{RETRY}.get_latest_session_state", side_effect=lambda *_, **__: session[0]),
        patch(f"{RECOVERY}.get_latest_session_state", side_effect=lambda *_, **__: session[0]),
    ):
        store = provider._get_initial_delivery_claims()
        assert store.claim(
            12,
            recovery_key,
            "recovery",
            {"head": HEAD, "initial_task_id": "initial-task", "diff": "ZERO_DIFF"},
        )
        recovery_path = f"/repos/org/repo/contents/.agdt/initial-delivery/12/{recovery_key}/recovery.json"
        recovery_record = json.loads(base64.b64decode(claims_fake.documents[recovery_path]))
        recovery_record["created_at"] = (datetime.now(UTC) - timedelta(hours=2)).isoformat()
        claims_fake.documents[recovery_path] = base64.b64encode(json.dumps(recovery_record).encode()).decode()

        action = RetryFailedSessionAction(provider, retry_limit=1)
        derived = DerivedState(snapshot)
        assert action.evaluate(snapshot, derived).decision is ActionDecision.EXECUTE
        assert action.execute(provider, snapshot, derived).decision is ActionDecision.EXECUTE
        notice = post_comment.call_args.args[1]
        assert f"<!-- agdt:agent-retry-escalation:{recovery_key} -->" in notice
        assert "<!-- agdt:agent-retry-escalation-pr:12 -->" not in notice
        comments.append(IssueCommentInfo(42, "workflow-bot", notice))

        provider.remove_label(12, AGENT_FAILED_LABEL)
        metadata[0] = replace(metadata[0], head_sha=DELIVERED_HEAD, changed_files=1)
        delivered = replace(
            snapshot,
            head_sha=DELIVERED_HEAD,
            initial_delivery=replace(evidence, outcome=InitialDeliveryOutcome.DELIVERED, head_sha=DELIVERED_HEAD),
        )
        session[0] = SessionState(SessionOutcome.FINISHED, task_id="recovery-task")
        delivered_action = RetryFailedSessionAction(provider, retry_limit=1)
        delivered_derived = DerivedState(delivered)
        assert delivered_action.evaluate(delivered, delivered_derived).decision is ActionDecision.SKIP

        session[0] = SessionState(SessionOutcome.FAILED, task_id="unrelated-task", failure_event_id=765)
        retry_action = RetryFailedSessionAction(provider, retry_limit=1)
        retry_derived = DerivedState(delivered)
        assert retry_action.evaluate(delivered, retry_derived).decision is ActionDecision.EXECUTE
        assert retry_derived.get("agent_retry_mode") == "retry"
        assert retry_action.execute(provider, delivered, retry_derived).decision is ActionDecision.EXECUTE

    remove_label.assert_called_once_with(12, AGENT_FAILED_LABEL)
    dispatch.assert_called_once()
    assert dispatch.call_args.args[2] == "unrelated-task"
    add_label.assert_called_once_with(12, AGENT_FAILED_LABEL)
