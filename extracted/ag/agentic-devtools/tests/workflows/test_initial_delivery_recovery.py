"""Cross-worker recovery with a shared atomic contents-API fake and real classifier."""

import base64
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlsplit

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.initial_delivery_claims import InitialDeliveryClaims
from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.pipeline.actions.initial_delivery_recovery import InitialDeliveryRecovery
from agentic_devtools.cli.ci.pipeline.actions.retry_failed_session import RetryFailedSessionAction
from agentic_devtools.cli.ci.pipeline.delivery import InitialDeliveryEvidence, InitialDeliveryOutcome
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError

RECOVERY = "agentic_devtools.cli.ci.pipeline.actions.initial_delivery_recovery"
RETRY = "agentic_devtools.cli.ci.pipeline.actions.retry_failed_session"
HEAD = "a" * 40


def _provider(metadata):
    provider = MagicMock()
    provider.get_pr_metadata.return_value = metadata
    provider.get_ref_sha.return_value = "c" * 40
    provider.list_pr_files_complete.return_value = []
    provider._get_initial_delivery_claims.side_effect = lambda: InitialDeliveryClaims("org/repo")
    provider._dispatch_agent_retry.return_value = 99
    provider.dispatch_agent_retry.side_effect = AssertionError("Recovery must not use public FAILED dispatch")
    provider.get_agent_task_prompt.return_value = "Implement the original issue"
    provider.get_dispatch_login.return_value = "workflow-bot"
    provider.list_issue_comments.return_value = []
    return provider


def _assert_ordinary_retry(provider, snapshot, documents):
    provider.dispatch_agent_retry.side_effect = None
    provider.dispatch_agent_retry.return_value = 101
    action = RetryFailedSessionAction(provider)
    derived = DerivedState(snapshot)
    result = action.evaluate(snapshot, derived)
    assert result.decision is ActionDecision.EXECUTE
    assert derived.get("agent_retry_mode") == "retry"
    assert action.execute(provider, snapshot, derived).decision is ActionDecision.EXECUTE
    provider.dispatch_agent_retry.assert_called_once()
    assert provider.dispatch_agent_retry.call_args.args[2] == "unrelated-task"
    provider._dispatch_agent_retry.assert_called_once()
    delivered_receipts = [
        json.loads(base64.b64decode(content)) for path, content in documents.items() if path.endswith("/delivered.json")
    ]
    assert {receipt["task_id"] for receipt in delivered_receipts} == {
        "recovery-task",
        "same-head-task",
        "repair-task",
    }


def _assert_single_initial_recovery(run, provider, documents):
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda _: run(concurrent=True), range(4)))
    assert provider._dispatch_agent_retry.call_count == len(documents) == 1
    assert run().decision is ActionDecision.BLOCKED and provider.add_label.call_count == 0

    path = next(iter(documents))
    record = json.loads(base64.b64decode(documents[path]))
    record["created_at"] = (datetime.now(UTC) - timedelta(hours=2)).isoformat()
    documents[path] = base64.b64encode(json.dumps(record).encode()).decode()
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda _: run(concurrent=True), range(4)))
    assert provider._dispatch_agent_retry.call_count == provider.post_comment_as_pr_token.call_count == 1
    assert len(documents) == 2


def _assert_same_head_delivery_reuse(run, provider, state):
    state[0] = SessionState(SessionOutcome.FINISHED, task_id="same-head-task")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda _: run(concurrent=True), range(4)))
    assert all(result.decision is ActionDecision.SKIP for result in results)
    assert run().decision is ActionDecision.SKIP

    state[0] = SessionState(SessionOutcome.FAILED, task_id="same-head-task", failure_event_id=124)
    assert run().decision is ActionDecision.BLOCKED
    provider.dispatch_agent_retry.assert_not_called()


class _CreateOnlyClaimsFake:
    def __init__(self, writer_on_claim="recovery"):
        self.documents = {}
        self.writer_started = False
        self.writer_on_claim = writer_on_claim

    def __call__(self, endpoint, *, method="GET", body=None):
        path = endpoint.split("?")[0]
        if method == "PUT":
            current = self.documents.get(path)
            current_sha = hashlib.sha256(current.encode()).hexdigest() if current is not None else None
            if body.get("sha") != current_sha:
                raise RuntimeError("HTTP 409 blob SHA conflict")
            self.documents[path] = body["content"]
            if current is None and self.writer_on_claim and path.endswith(f"/{self.writer_on_claim}.json"):
                self.writer_started = True
            return "{}"
        if path not in self.documents:
            raise RuntimeError("HTTP 404")
        return json.dumps(
            {
                "content": self.documents[path],
                "sha": hashlib.sha256(self.documents[path].encode()).hexdigest(),
            }
        )


class _FakeAgentTaskRest:
    def __init__(self, claims, head_branch):
        self.claims = claims
        self.head_branch = head_branch
        self.calls = []

    def __call__(self, endpoint, **_kwargs):
        self.calls.append(endpoint)
        if "/agents/repos/" in endpoint and "/tasks?" in endpoint:
            return json.dumps({"tasks": []})
        if "/actions/workflows?" in endpoint and "/runs?" not in endpoint:
            return json.dumps({"workflows": [{"id": 42, "path": "dynamic/copilot-swe-agent/copilot.yml"}]})
        if "/actions/workflows/42/runs?" in endpoint:
            return self._runs(endpoint)
        raise AssertionError(f"Unexpected REST endpoint: {endpoint}")

    def _runs(self, endpoint):
        status = parse_qs(urlsplit(endpoint).query)["status"][0]
        if not self.claims.writer_started or status != "in_progress":
            return json.dumps({"workflow_runs": []})
        now = datetime.now(UTC).isoformat()
        return json.dumps(
            {
                "workflow_runs": [
                    {
                        "id": 99,
                        "status": "in_progress",
                        "run_attempt": 1,
                        "created_at": now,
                        "run_started_at": now,
                        "event": "push",
                        "repository": {"full_name": "org/repo"},
                        "head_branch": self.head_branch,
                        "head_sha": HEAD,
                        "pull_requests": [{"number": 12}],
                    }
                ]
            }
        )


def test_same_head_writer_start_invalidates_cached_lifecycle_and_run_inventories(monkeypatch) -> None:
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
    metadata = PRMetadata(
        12,
        "Task",
        snapshot.head_branch,
        HEAD,
        "main",
        head_repo_full_name="org/repo",
        base_repo_full_name="org/repo",
        changed_files=0,
    )
    state = SessionState(SessionOutcome.FINISHED, task_id="initial-task")
    claims_fake = _CreateOnlyClaimsFake()
    github_api = _FakeAgentTaskRest(claims_fake, snapshot.head_branch)

    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=github_api),
        patch.object(InitialDeliveryClaims, "_api", side_effect=claims_fake),
        patch.object(provider, "get_pr_metadata", return_value=metadata),
        patch.object(provider, "get_agent_task_prompt", return_value="Implement the original issue"),
        patch.object(provider, "list_closing_issues", return_value=[]),
        patch.object(provider, "get_pr_body", return_value=""),
        patch.object(provider, "_dispatch_agent_retry") as dispatch,
        patch.object(provider, "add_label") as add_label,
        patch.object(provider, "post_comment_as_pr_token") as post_comment,
        patch(f"{RETRY}.get_latest_session_state", return_value=state),
        patch(f"{RECOVERY}.get_latest_session_state", return_value=state),
        patch(
            f"{RECOVERY}.classify_initial_delivery_with_head",
            return_value=(HEAD, InitialDeliveryOutcome.NO_DELIVERY),
        ),
    ):
        action = RetryFailedSessionAction(provider)
        derived = DerivedState(snapshot)
        evaluation = action.evaluate(snapshot, derived)
        assert evaluation.decision is ActionDecision.EXECUTE, f"{evaluation.details}: {github_api.calls}"
        result = action.execute(provider, snapshot, derived)

    assert claims_fake.writer_started is True
    assert result.decision is ActionDecision.BLOCKED
    dispatch.assert_not_called()
    add_label.assert_not_called()
    post_comment.assert_not_called()


def test_classifier_head_mismatch_blocks_an_a_to_b_to_a_handoff() -> None:
    metadata_a = PRMetadata(
        12,
        "Task",
        "copilot/feature",
        HEAD,
        "main",
        head_repo_full_name="org/repo",
        base_repo_full_name="org/repo",
        changed_files=1,
    )
    metadata_b = replace(metadata_a, head_sha="b" * 40)
    provider = _provider(metadata_a)
    provider.get_pr_metadata.side_effect = [metadata_a, metadata_b, metadata_b, metadata_a]
    provider.list_pr_files_complete.return_value = ["src/app.py"]
    claims = MagicMock()
    claims.read.return_value = {"created_at": datetime.now(UTC).isoformat()}
    provider._get_initial_delivery_claims.side_effect = lambda: claims
    snapshot = PRStateSnapshot(
        pr_number=12,
        head_sha=HEAD,
        head_branch="copilot/feature",
        head_repo_full_name="org/repo",
        base_repo_full_name="org/repo",
        initial_delivery=InitialDeliveryEvidence(InitialDeliveryOutcome.NO_DELIVERY, "initial-task", HEAD, HEAD),
    )
    state = SessionState(SessionOutcome.FINISHED, task_id="recovery-task")

    with (
        patch(f"{RETRY}.get_latest_session_state", return_value=state),
        patch(f"{RECOVERY}.is_copilot_session_active_via_agent_task", return_value=False),
    ):
        action = RetryFailedSessionAction(provider)
        result = action.evaluate(snapshot, DerivedState(snapshot))

    assert result.decision is ActionDecision.BLOCKED
    claims.claim.assert_not_called()
    provider._dispatch_agent_retry.assert_not_called()


def test_writer_start_before_escalation_claim_leaves_notice_retryable(monkeypatch) -> None:
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
    metadata = PRMetadata(
        12,
        "Task",
        snapshot.head_branch,
        HEAD,
        "main",
        head_repo_full_name="org/repo",
        base_repo_full_name="org/repo",
        changed_files=0,
    )
    state = SessionState(SessionOutcome.FAILED, task_id="recovery-task")
    claims_fake = _CreateOnlyClaimsFake()
    github_api = _FakeAgentTaskRest(claims_fake, snapshot.head_branch)
    recovery_key = InitialDeliveryRecovery._identity(evidence)
    claim_path = f"/repos/org/repo/contents/.agdt/initial-delivery/12/{recovery_key}/recovery.json"

    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=github_api),
        patch.object(InitialDeliveryClaims, "_api", side_effect=claims_fake),
        patch.object(provider, "get_pr_metadata", return_value=metadata),
        patch.object(provider, "list_issue_comments", return_value=[]),
        patch.object(provider, "get_dispatch_login", return_value="workflow-bot"),
        patch.object(provider, "post_comment_as_pr_token") as post_comment,
        patch.object(provider, "add_label") as add_label,
        patch(f"{RETRY}.get_latest_session_state", return_value=state),
        patch(f"{RECOVERY}.get_latest_session_state", return_value=state),
        patch(
            f"{RECOVERY}.classify_initial_delivery_with_head",
            return_value=(HEAD, InitialDeliveryOutcome.UNKNOWN),
        ),
    ):
        store = provider._get_initial_delivery_claims()
        assert store.claim(12, recovery_key, "recovery", {})
        record = json.loads(base64.b64decode(claims_fake.documents[claim_path]))
        record["created_at"] = (datetime.now(UTC) - timedelta(hours=2)).isoformat()
        claims_fake.documents[claim_path] = base64.b64encode(json.dumps(record).encode()).decode()
        claims_fake.writer_started = False
        invalidate = provider.invalidate_agent_task_inventory
        observations = 0

        def invalidate_then_start_writer(pr_number=None):
            nonlocal observations
            observations += 1
            if observations == 4:
                claims_fake.writer_started = True
            invalidate(pr_number)

        with patch.object(provider, "invalidate_agent_task_inventory", side_effect=invalidate_then_start_writer):

            def run():
                action = RetryFailedSessionAction(provider)
                derived = DerivedState(snapshot)
                assert action.evaluate(snapshot, derived).decision is ActionDecision.EXECUTE
                return action.execute(provider, snapshot, derived)

            assert run().decision is ActionDecision.BLOCKED
            assert observations == 4
            assert not any(path.endswith("/escalation.json") for path in claims_fake.documents)
            post_comment.assert_not_called()
            add_label.assert_not_called()

            claims_fake.writer_started = False
            assert run().decision is ActionDecision.EXECUTE

    assert sum(path.endswith("/escalation.json") for path in claims_fake.documents) == 1
    post_comment.assert_called_once()
    add_label.assert_called_once_with(12, "ai-pr-loop:agent-failed")


def test_writer_start_during_escalation_reservation_is_released_and_retried(monkeypatch) -> None:
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
    metadata = PRMetadata(
        12,
        "Task",
        snapshot.head_branch,
        HEAD,
        "main",
        head_repo_full_name="org/repo",
        base_repo_full_name="org/repo",
        changed_files=0,
    )
    state = SessionState(SessionOutcome.FAILED, task_id="recovery-task")
    claims_fake = _CreateOnlyClaimsFake(writer_on_claim="escalation")
    github_api = _FakeAgentTaskRest(claims_fake, snapshot.head_branch)
    recovery_key = InitialDeliveryRecovery._identity(evidence)
    recovery_path = f"/repos/org/repo/contents/.agdt/initial-delivery/12/{recovery_key}/recovery.json"
    escalation_path = f"/repos/org/repo/contents/.agdt/initial-delivery/12/{recovery_key}/escalation.json"

    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=github_api),
        patch.object(InitialDeliveryClaims, "_api", side_effect=claims_fake),
        patch.object(provider, "get_pr_metadata", return_value=metadata),
        patch.object(provider, "list_issue_comments", return_value=[]),
        patch.object(provider, "get_dispatch_login", return_value="workflow-bot"),
        patch.object(provider, "post_comment_as_pr_token") as post_comment,
        patch.object(provider, "add_label") as add_label,
        patch(f"{RETRY}.get_latest_session_state", return_value=state),
        patch(f"{RECOVERY}.get_latest_session_state", return_value=state),
        patch(
            f"{RECOVERY}.classify_initial_delivery_with_head",
            return_value=(HEAD, InitialDeliveryOutcome.UNKNOWN),
        ),
    ):
        store = provider._get_initial_delivery_claims()
        assert store.claim(12, recovery_key, "recovery", {"head": HEAD})
        record = json.loads(base64.b64decode(claims_fake.documents[recovery_path]))
        record["created_at"] = (datetime.now(UTC) - timedelta(hours=2)).isoformat()
        claims_fake.documents[recovery_path] = base64.b64encode(json.dumps(record).encode()).decode()

        def run():
            action = RetryFailedSessionAction(provider)
            derived = DerivedState(snapshot)
            assert action.evaluate(snapshot, derived).decision is ActionDecision.EXECUTE
            return action.execute(provider, snapshot, derived)

        assert run().decision is ActionDecision.BLOCKED
        reserved = json.loads(base64.b64decode(claims_fake.documents[escalation_path]))
        assert reserved["stage"] == "retryable"
        assert post_comment.call_count == add_label.call_count == 0
        assert claims_fake.writer_started is True

        claims_fake.writer_started = False
        assert run().decision is ActionDecision.EXECUTE
        attempted = json.loads(base64.b64decode(claims_fake.documents[escalation_path]))
        assert attempted["stage"] == "attempted"

    assert post_comment.call_count == add_label.call_count == 1


@pytest.mark.parametrize(
    "post_error",
    [
        TimeoutError("response lost"),
        RetryableError("response lost"),
        RuntimeError("provider rejected"),
        ProviderRateLimitError(retry_after_seconds=30, provider="github", credential_identity="notice"),
    ],
)
def test_ambiguous_escalation_post_stays_fenced_after_provider_restart(monkeypatch, post_error) -> None:
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
    metadata = PRMetadata(
        12,
        "Task",
        snapshot.head_branch,
        HEAD,
        "main",
        head_repo_full_name="org/repo",
        base_repo_full_name="org/repo",
        changed_files=0,
    )
    state = SessionState(SessionOutcome.FAILED, task_id="recovery-task")
    claims_fake = _CreateOnlyClaimsFake(writer_on_claim=None)
    recovery_key = InitialDeliveryRecovery._identity(evidence)
    recovery_path = f"/repos/org/repo/contents/.agdt/initial-delivery/12/{recovery_key}/recovery.json"
    escalation_path = f"/repos/org/repo/contents/.agdt/initial-delivery/12/{recovery_key}/escalation.json"

    with (
        patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            side_effect=_FakeAgentTaskRest(claims_fake, "copilot/feature"),
        ),
        patch.object(InitialDeliveryClaims, "_api", side_effect=claims_fake),
        patch(f"{RETRY}.get_latest_session_state", return_value=state),
        patch(f"{RECOVERY}.get_latest_session_state", return_value=state),
        patch(
            f"{RECOVERY}.classify_initial_delivery_with_head",
            return_value=(HEAD, InitialDeliveryOutcome.UNKNOWN),
        ),
    ):
        assert InitialDeliveryClaims("org/repo").claim(12, recovery_key, "recovery", {"head": HEAD})
        recovery_record = json.loads(base64.b64decode(claims_fake.documents[recovery_path]))
        recovery_record["created_at"] = (datetime.now(UTC) - timedelta(hours=2)).isoformat()
        claims_fake.documents[recovery_path] = base64.b64encode(json.dumps(recovery_record).encode()).decode()
        with (
            patch.object(provider, "get_pr_metadata", return_value=metadata),
            patch.object(provider, "list_issue_comments", return_value=[]),
            patch.object(provider, "get_dispatch_login", return_value="workflow-bot"),
            patch.object(provider, "post_comment_as_pr_token", side_effect=post_error) as post_comment,
            patch.object(provider, "add_label") as add_label,
        ):
            action, derived = RetryFailedSessionAction(provider), DerivedState(snapshot)
            assert action.evaluate(snapshot, derived).decision is ActionDecision.EXECUTE
            if isinstance(post_error, ProviderRateLimitError):
                with pytest.raises(ProviderRateLimitError) as exc_info:
                    action.execute(provider, snapshot, derived)
                assert exc_info.value.retry_after_seconds == 30
            else:
                assert action.execute(provider, snapshot, derived).decision is ActionDecision.FAILED
            attempted = json.loads(base64.b64decode(claims_fake.documents[escalation_path]))
            assert attempted["stage"] == "attempted" and post_comment.call_count == 1 and add_label.call_count == 0

        restarted_provider = GitHubActionsProvider(repo="org/repo")
        with (
            patch.object(restarted_provider, "get_pr_metadata", return_value=metadata),
            patch.object(restarted_provider, "list_issue_comments", return_value=[]),
            patch.object(restarted_provider, "get_dispatch_login", return_value="workflow-bot"),
            patch.object(restarted_provider, "post_comment_as_pr_token") as restarted_post,
            patch.object(restarted_provider, "add_label") as restarted_label,
        ):
            restarted_action = RetryFailedSessionAction(restarted_provider)
            restarted_derived = DerivedState(snapshot)
            assert restarted_action.evaluate(snapshot, restarted_derived).decision is ActionDecision.EXECUTE
            assert (
                restarted_action.execute(restarted_provider, snapshot, restarted_derived).decision
                is ActionDecision.FAILED
            )
            assert restarted_post.call_count == restarted_label.call_count == 0
