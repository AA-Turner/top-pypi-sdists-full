"""Tests for run_pipeline."""

import base64
import hashlib
import json
import logging
import os
import zlib
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import cast
from unittest.mock import MagicMock, call, patch

import pytest

from agentic_devtools.cli.ci.approver_preflight import ApproverPreflightResult, CapabilityEvidence, EvidenceStatus
from agentic_devtools.cli.ci.models import (
    AgentTaskInventory,
    AgentTaskLifecycle,
    AgentTaskSessionLifecycle,
    IssueCommentInfo,
    IssueEvent,
    ReviewCommentInfo,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.actions import (
    ApproveAction,
    DispatchRepairAction,
    GuardsAction,
    MergeAction,
    PublishAction,
    RequestReviewAction,
    ResolveThreadsAction,
    RetryFailedSessionAction,
    SquashAction,
)
from agentic_devtools.cli.ci.pipeline.base import Action
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_HAS_COMMENTS,
    REASON_SUPPRESSED_COMMENTS,
    CopilotGateVerdict,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.runner import (
    DiffPreservationBlockerLookupError,
    _find_recent_conflict_repair_head,
    _find_recent_diff_preservation_blocker,
    _log_endgroup,
    _log_group,
    run_pipeline,
)
from agentic_devtools.cli.ci.pipeline.session_detector import (
    SessionOutcome,
    SessionState,
    reconcile_agent_task_lifecycles,
)
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.reconciliation.models import CloudWriterRunInventory, WorkflowRun
from agentic_devtools.cli.shared.retry import ProviderRateLimitError
from tests.unit.cli.ci.pipeline._runner_fixtures import _diff_preservation_blocker_comment, _MockAction
from tests.unit.cli.ci.pipeline._verified_pr_provider import verified_pr_provider


class TestRunPipeline:
    """Tests for the pipeline runner."""

    @pytest.mark.parametrize("existing_precise_approval", [False, True])
    def test_preflight_block_preserves_independent_precise_merge_policy(self, existing_precise_approval) -> None:
        verified = CapabilityEvidence(EvidenceStatus.VERIFIED, "bot", 200)
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head",
            ci_status="passing",
            labels=["ai-auto-merge-allowed"],
            mergeable=True,
            review_state="APPROVED",
            copilot_review_id=2,
            approver_login="bot",
            has_approval_on_head=True,
            has_approver_approval_on_head=existing_precise_approval,
            approver_preflight=ApproverPreflightResult(verified, verified, verified),
        )
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "head"
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.merge.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            summary = run_pipeline(
                provider,
                snapshot,
                [
                    _MockAction("guards", ActionDecision.EXECUTE),
                    ApproveAction(),
                    MergeAction(),
                ],
            )
        assert summary.results[1].decision is ActionDecision.BLOCKED
        assert summary.results[1].capability == "review_eligibility"
        expected = ActionDecision.EXECUTE if existing_precise_approval else ActionDecision.SKIP
        assert summary.results[2].decision is expected
        assert provider.merge_pr.call_count == int(existing_precise_approval)
        provider.approve_pr.assert_not_called()
        assert snapshot.has_approver_approval_on_head is existing_precise_approval

    @pytest.fixture(autouse=True)
    def mock_lifecycle_reconciliation(self):
        """Keep runner unit tests isolated from lifecycle provider mutations."""
        with patch("agentic_devtools.cli.ci.pipeline.runner.reconcile_agent_task_lifecycles"):
            yield

    def test_reconciles_before_unknown_lifecycle_guard(self):
        snapshot = PRStateSnapshot(pr_number=42, base_repo_full_name="owner/repo", head_sha="head")
        provider = MagicMock()
        action = MagicMock()
        action.name = "approve"
        action.evaluate.return_value = ActionResult("approve", ActionDecision.SKIP)
        events = []
        provider.invalidate_agent_task_inventory.side_effect = lambda pr: events.append("invalidate")
        action.evaluate.side_effect = lambda *args: (
            events.append("evaluate") or ActionResult("approve", ActionDecision.SKIP)
        )
        with patch("agentic_devtools.cli.ci.pipeline.runner.reconcile_agent_task_lifecycles", create=True) as reconcile:
            reconcile.side_effect = lambda *args, **kwargs: events.append("reconcile")
            run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.EXECUTE), action])
        assert events == ["invalidate", "reconcile", "evaluate"]
        reconcile.assert_called_once_with(
            "owner/repo", 42, head_branch="", head_sha="head", pr_id=None, provider=provider
        )
        action.execute.assert_not_called()

    def test_guard_block_prevents_lifecycle_reconciliation(self):
        with patch("agentic_devtools.cli.ci.pipeline.runner.reconcile_agent_task_lifecycles", create=True) as reconcile:
            run_pipeline(
                MagicMock(),
                PRStateSnapshot(pr_number=42),
                [_MockAction("guards", ActionDecision.BLOCKED), _MockAction("approve", ActionDecision.EXECUTE)],
            )
        reconcile.assert_not_called()

    def test_guard_block_prevents_retry_and_lifecycle_reconciliation(self):
        with patch("agentic_devtools.cli.ci.pipeline.runner.reconcile_agent_task_lifecycles", create=True) as reconcile:
            run_pipeline(
                MagicMock(),
                PRStateSnapshot(pr_number=42),
                [
                    _MockAction("guards", ActionDecision.BLOCKED),
                    _MockAction("retry_failed_session", ActionDecision.SKIP),
                    _MockAction("approve", ActionDecision.EXECUTE),
                ],
            )
        reconcile.assert_not_called()

    def test_retry_after_guards_continues_after_expired_lifecycle(self):
        snapshot = PRStateSnapshot(
            pr_number=42,
            base_repo_full_name="owner/repo",
            head_repo_full_name="owner/repo",
            head_sha="head",
            title="Feature",
            files=["src/feature.py"],
        )
        provider = MagicMock()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.retry_failed_session.get_latest_session_state",
            return_value=SessionState(SessionOutcome.EXPIRED, task_id="old-task"),
        ):
            summary = run_pipeline(
                provider,
                snapshot,
                [
                    GuardsAction(),
                    RetryFailedSessionAction(provider),
                    _MockAction("approve", ActionDecision.EXECUTE),
                ],
            )

        assert [result.decision for result in summary.results] == [
            ActionDecision.EXECUTE,
            ActionDecision.SKIP,
            ActionDecision.EXECUTE,
        ]

    def test_resolve_threads_rechecks_lifecycle_when_writer_starts_after_retry_skips(self):
        provider = MagicMock()
        snapshot = PRStateSnapshot(
            pr_number=42,
            base_repo_full_name="owner/repo",
            head_repo_full_name="owner/repo",
            head_sha="head",
            head_branch="copilot/feature",
            title="Feature",
            files=["src/feature.py"],
            ci_status="passing",
            unresolved_threads=1,
            repairable_threads=1,
        )
        retry_action = RetryFailedSessionAction(provider)
        initial_state = SessionState(SessionOutcome.EXPIRED, task_id="old-task")

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.retry_failed_session.get_latest_session_state",
                return_value=initial_state,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.resolve_threads.is_copilot_session_active_via_agent_task",
                side_effect=[False, True],
            ),
        ):
            summary = run_pipeline(
                provider,
                snapshot,
                [
                    GuardsAction(phase="safety"),
                    retry_action,
                    ResolveThreadsAction(),
                ],
            )

        assert [result.decision for result in summary.results] == [
            ActionDecision.EXECUTE,
            ActionDecision.SKIP,
            ActionDecision.BLOCKED,
        ]
        provider.finalize_post_repair.assert_not_called()

    def test_reconciles_missing_clock_before_retry_resolves_active_task(self):
        class ProviderWithTasks(MagicMock):
            def list_agent_tasks(self, repo: str) -> list[object]:
                assert repo == "owner/repo"
                return [{"id": "task-abc", "state": "in_progress", "pullRequestNumber": 42}]

        provider = ProviderWithTasks()
        provider.get_pr_metadata.return_value = SimpleNamespace(head_sha="head")
        provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
            (
                AgentTaskLifecycle(
                    task_id="task-abc",
                    repository="owner/repo",
                    pr_number=42,
                    head_branch="copilot/feature",
                    state="in_progress",
                    created_at="malformed",
                ),
            )
        )
        recorded_at = datetime.now(UTC).isoformat()
        provider.get_or_record_agent_task_first_observed_at.return_value = recorded_at
        provider.get_agent_task_first_observed_at.return_value = recorded_at
        provider.list_correlated_cloud_writer_runs = None
        provider.cancel_workflow_run = None
        snapshot = PRStateSnapshot(
            pr_number=42,
            base_repo_full_name="owner/repo",
            head_repo_full_name="owner/repo",
            head_branch="copilot/feature",
            head_sha="head",
            title="Feature",
            files=["src/feature.py"],
        )

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.reconcile_agent_task_lifecycles",
            side_effect=reconcile_agent_task_lifecycles,
        ):
            summary = run_pipeline(
                provider,
                snapshot,
                [
                    GuardsAction(phase="safety"),
                    RetryFailedSessionAction(provider),
                    GuardsAction(phase="progression"),
                ],
            )

        assert [result.decision for result in summary.results] == [
            ActionDecision.EXECUTE,
            ActionDecision.BLOCKED,
            ActionDecision.BLOCKED_BY_GUARD,
        ]
        provider.get_or_record_agent_task_first_observed_at.assert_called_once_with(
            42,
            task_id="task-abc",
            session_id="",
            head_branch="copilot/feature",
            expected_head_sha="head",
        )

    def test_retry_is_rechecked_after_lifecycle_reconciliation(self):
        snapshot = PRStateSnapshot(
            pr_number=42,
            base_repo_full_name="owner/repo",
            head_repo_full_name="owner/repo",
            head_sha="head",
            title="Feature",
            files=["src/feature.py"],
        )
        provider = MagicMock()
        provider.get_dispatch_login.return_value = "workflow-bot"
        provider.list_issue_comments.return_value = []
        retry_action = RetryFailedSessionAction(provider, retry_limit=1)
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.retry_failed_session.get_latest_session_state",
            side_effect=[
                SessionState(SessionOutcome.FAILED, task_id="failed-task"),
                SessionState(SessionOutcome.ACTIVE, task_id="failed-task"),
            ],
        ) as get_latest:
            summary = run_pipeline(
                provider,
                snapshot,
                [
                    GuardsAction(phase="safety"),
                    retry_action,
                    GuardsAction(phase="progression"),
                    _MockAction("resolve_threads", ActionDecision.EXECUTE),
                ],
            )

        assert [result.decision for result in summary.results] == [
            ActionDecision.EXECUTE,
            ActionDecision.BLOCKED,
            ActionDecision.BLOCKED_BY_GUARD,
            ActionDecision.BLOCKED_BY_GUARD,
        ]
        assert get_latest.call_count == 2
        provider.dispatch_agent_retry.assert_not_called()

    @pytest.mark.parametrize("writer_evidence", ["young", "incomplete"])
    def test_timeline_failure_retry_is_blocked_by_final_aggregate_lifecycle_check(self, writer_evidence):
        class ProviderWithTimelineFailure(MagicMock):
            def list_agent_tasks(self, repo):
                assert repo == "owner/repo"
                return []

        provider = ProviderWithTimelineFailure()
        provider.get_dispatch_login.return_value = "workflow-bot"
        provider.list_issue_comments.return_value = []
        provider.list_pr_issue_events.return_value = [
            IssueEvent(42, "copilot_work_finished_failure", "2026-10-16T00:01:00Z")
        ]
        provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(())
        young_writer_inventory = CloudWriterRunInventory(
            runs=(
                WorkflowRun(
                    id=101,
                    name="Copilot Writer",
                    conclusion="",
                    run_attempt=1,
                    created_at=datetime.now(UTC).isoformat(),
                    event="workflow_dispatch",
                    head_branch="copilot/feature",
                    status="in_progress",
                    run_started_at=datetime.now(UTC).isoformat(),
                ),
            )
        )
        protective_inventory = (
            young_writer_inventory
            if writer_evidence == "young"
            else CloudWriterRunInventory(complete=False, incomplete_reasons=("page-limit",))
        )
        provider.list_correlated_cloud_writer_runs.side_effect = [
            CloudWriterRunInventory(),
            protective_inventory,
        ]
        snapshot = PRStateSnapshot(
            pr_number=42,
            base_repo_full_name="owner/repo",
            head_repo_full_name="owner/repo",
            head_branch="copilot/feature",
            head_sha="head",
            title="Feature",
            files=["src/feature.py"],
        )

        summary = run_pipeline(
            provider,
            snapshot,
            [
                GuardsAction(phase="safety"),
                RetryFailedSessionAction(provider, retry_limit=1),
                _MockAction("approve", ActionDecision.EXECUTE),
            ],
        )

        assert [result.decision for result in summary.results] == [
            ActionDecision.EXECUTE,
            ActionDecision.BLOCKED,
            ActionDecision.BLOCKED_BY_GUARD,
        ]
        if writer_evidence == "young":
            assert summary.results[1].preconditions == {"session_active": True}
        else:
            assert summary.results[1].preconditions == {"session_outcome_known": False}
        provider.dispatch_agent_retry.assert_not_called()

    def test_retry_is_blocked_by_younger_session_under_failed_task(self):
        provider = MagicMock()
        provider.list_pr_issue_events.return_value = []
        provider.list_pr_agent_task_lifecycles.return_value = AgentTaskInventory(
            (
                AgentTaskLifecycle(
                    task_id="failed-task",
                    repository="owner/repo",
                    pr_number=42,
                    head_branch="copilot/feature",
                    state="failed",
                    created_at="2026-10-16T00:00:00Z",
                    sessions=(
                        AgentTaskSessionLifecycle(
                            session_id="running-child",
                            state="in_progress",
                            started_at=datetime.now(UTC).isoformat(),
                        ),
                    ),
                ),
            )
        )
        provider.list_correlated_cloud_writer_runs.return_value = CloudWriterRunInventory()
        task = {
            "id": "failed-task",
            "state": "failed",
            "pullRequestNumber": 42,
            "createdAt": "2026-10-16T00:00:00Z",
            "updatedAt": "2026-10-16T00:01:00Z",
        }
        retry_action = RetryFailedSessionAction(provider, retry_limit=1)
        snapshot = PRStateSnapshot(
            pr_number=42,
            base_repo_full_name="owner/repo",
            head_repo_full_name="owner/repo",
            head_branch="copilot/feature",
            head_sha="head",
            title="Feature",
            files=["src/feature.py"],
        )

        with patch(
            "agentic_devtools.cli.ci.agent_task_inventory.run_safe",
            return_value=SimpleNamespace(returncode=0, stdout=json.dumps({"tasks": [task]}), stderr=""),
        ):
            summary = run_pipeline(
                provider,
                snapshot,
                [
                    GuardsAction(phase="safety"),
                    retry_action,
                    GuardsAction(phase="progression"),
                    _MockAction("resolve_threads", ActionDecision.EXECUTE),
                ],
            )

        assert [result.decision for result in summary.results] == [
            ActionDecision.EXECUTE,
            ActionDecision.BLOCKED,
            ActionDecision.BLOCKED_BY_GUARD,
            ActionDecision.BLOCKED_BY_GUARD,
        ]
        provider.dispatch_agent_retry.assert_not_called()

    @pytest.mark.parametrize(
        ("title", "files"),
        [
            ("[WIP] unfinished work", ["src/feature.py"]),
            ("Feature", []),
        ],
        ids=["wip-pr", "empty-pr"],
    )
    def test_failed_session_recovery_precedes_progression_gates(self, title, files):
        snapshot = PRStateSnapshot(
            pr_number=42,
            base_repo_full_name="owner/repo",
            head_repo_full_name="owner/repo",
            head_sha="head",
            title=title,
            files=files,
            is_draft=True,
        )
        provider = MagicMock()
        provider.get_dispatch_login.return_value = "workflow-bot"
        provider.list_issue_comments.return_value = []
        provider.get_agent_task_prompt.return_value = "Original task"
        retry_action = RetryFailedSessionAction(provider, retry_limit=1)

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.retry_failed_session.get_latest_session_state",
            return_value=SessionState(SessionOutcome.FAILED, task_id="failed-task"),
        ):
            summary = run_pipeline(
                provider,
                snapshot,
                [
                    GuardsAction(phase="safety"),
                    retry_action,
                    GuardsAction(phase="progression"),
                ],
            )

        assert [result.name for result in summary.results] == ["safety_guards", "retry_failed_session", "guards"]
        assert [result.decision for result in summary.results] == [
            ActionDecision.EXECUTE,
            ActionDecision.EXECUTE,
            ActionDecision.SKIP,
        ]
        provider.dispatch_agent_retry.assert_called_once()

    @pytest.mark.parametrize(
        "name", ["approve", "merge", "request_review", "dispatch_repair", "publish", "dispatch_conflict_resolution"]
    )
    def test_new_same_head_writer_blocks_final_action(self, name):
        snapshot = PRStateSnapshot(pr_number=42, base_repo_full_name="owner/repo", head_sha="head")
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = snapshot.head_sha
        action = MagicMock()
        action.name = name
        action.may_invalidate_snapshot = name == "publish"
        events = []
        provider.invalidate_agent_task_inventory.side_effect = lambda pr: events.append("invalidate")
        decisions = iter([ActionDecision.EXECUTE, ActionDecision.SKIP])
        action.evaluate.side_effect = lambda *args: events.append("evaluate") or ActionResult(name, next(decisions))
        with patch("agentic_devtools.cli.ci.pipeline.runner.reconcile_agent_task_lifecycles", create=True) as reconcile:
            reconcile.side_effect = lambda *args, **kwargs: events.append("reconcile")
            summary = run_pipeline(provider, snapshot, [action])
        assert events == ["invalidate", "reconcile", "evaluate", "invalidate", "reconcile", "invalidate", "evaluate"]
        assert summary.results[0].decision == ActionDecision.SKIP
        action.execute.assert_not_called()

    @pytest.mark.parametrize("raises", [False, True])
    @pytest.mark.parametrize("supports_invalidation", [False, True])
    def test_dispatch_invalidates_inventory_even_when_execution_fails(self, raises, supports_invalidation):
        provider = MagicMock()
        if not supports_invalidation:
            provider.invalidate_agent_task_inventory = None
        action = MagicMock()
        action.name = "dispatch_repair"
        action.may_invalidate_snapshot = False
        action.evaluate.return_value = ActionResult("dispatch_repair", ActionDecision.EXECUTE)
        action.execute.return_value = ActionResult("dispatch_repair", ActionDecision.EXECUTE)
        if raises:
            action.execute.side_effect = RuntimeError("uncertain dispatch")
        with patch("agentic_devtools.cli.ci.pipeline.runner.reconcile_agent_task_lifecycles", create=True):
            run_pipeline(provider, PRStateSnapshot(pr_number=42), [action])
        if supports_invalidation:
            assert provider.invalidate_agent_task_inventory.call_args_list == [call(42)] * 4
        action.execute.assert_called_once()

    def test_exhausted_dispatch_is_not_a_productive_action_or_a_cleared_finding(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="head",
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            unresolved_threads=2,
        )
        action = MagicMock()
        action.name = "dispatch_repair"
        action.may_invalidate_snapshot = False
        action.evaluate.return_value = ActionResult("dispatch_repair", ActionDecision.EXECUTE)
        action.execute.return_value = ActionResult(
            "dispatch_repair",
            ActionDecision.SKIP,
            limit_reached=True,
            dedup_limit_reached=True,
            repair_exhaustion_marker="exhausted-scope",
        )
        summary = run_pipeline(MagicMock(), snapshot, actions=[action])
        assert summary.results[0].decision is ActionDecision.SKIP
        assert summary.results[0].repair_exhaustion_marker == "exhausted-scope"
        assert summary.snapshot is not None
        assert summary.snapshot.unresolved_threads == 2

    @pytest.mark.parametrize(
        "hash_error",
        [RuntimeError("repair fingerprint failed"), ProviderRateLimitError(is_rate_limit=False)],
    )
    def test_historical_repair_hash_failure_uses_matching_exact_diffs(self, hash_error, caplog):
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body="<!-- agdt:conflict-repair:abc123:def456:2026-10-14T10:55:00Z -->",
            )
        ]
        provider.list_pr_commits.return_value = [
            {"sha": "def456"},
            {"sha": "repair", "parents": [{"sha": "def456"}]},
            {"sha": "feedbeef"},
        ]
        provider.compute_diff_files.return_value = ["fix.py"]
        provider.compute_diff_hash.side_effect = [hash_error, "baseline-hash"]
        provider.get_commit_range_diff_bytes.return_value = (
            b"diff --git a/fix.py b/fix.py\n--- a/fix.py\n+++ b/fix.py\n@@ -1 +1 @@\n-old\n+new\n"
        )
        provider.get_commit_range_diff_change_counts.return_value = {"fix.py": 2}
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py", "followup.py"],
            diff_hash="intentional-followup",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])
        assert summary.results[0].decision == ActionDecision.SKIP
        assert "Failed to compute repair-output fingerprint" in caplog.text
        provider.get_commit_range_diff_bytes.assert_has_calls(
            [call("pinned-base", "def456"), call("pinned-base", "repair")]
        )
        provider.post_comment.assert_called_once_with(1, "<!-- agdt:conflict-repair-validated:feedbeef -->")

    @pytest.mark.parametrize("repair_head", ["repair", "feedbeef"])
    @pytest.mark.parametrize(
        "failure",
        [
            "",
            "missing",
            "changed",
            "unavailable",
            "files-none",
            "files-invalid",
            "files-error",
            "hash-none",
            "hash-empty",
            "hash-error",
            "files-rate-limit",
            "hash-rate-limit",
        ],
    )
    def test_validates_repair_output_not_intentional_followups(self, repair_head, failure):
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body="<!-- agdt:conflict-repair:abc123:def456:2026-10-14T10:55:00Z -->",
            )
        ]
        provider.list_pr_commits.return_value = [
            {"sha": "def456"},
            {"sha": repair_head, "parents": [{"sha": "def456"}]},
            *([] if repair_head == "feedbeef" else [{"sha": "F1"}, {"sha": "feedbeef"}]),
        ]
        if failure == "unavailable":
            provider.list_pr_commits.side_effect = RuntimeError("commit list unavailable")
        provider.compute_diff_hash.side_effect = lambda **kw: (
            "intentional-followup"
            if kw["sha"] == "feedbeef" and repair_head != "feedbeef"
            else "changed-patch"
            if kw["sha"] == repair_head and failure == "changed"
            else "preserved"
        )
        provider.compute_diff_files.side_effect = lambda **kw: (
            ["fix.py"] if kw["sha"] == repair_head and failure == "missing" else ["fix.py", "keep.py"]
        )
        if repair_head != "feedbeef":
            if failure in {"files-none", "files-invalid"}:
                provider.compute_diff_files.side_effect = None
                provider.compute_diff_files.return_value = None if failure == "files-none" else [None]
            if failure in {"hash-none", "hash-empty"}:
                provider.compute_diff_hash.side_effect = None
                provider.compute_diff_hash.return_value = None if failure == "hash-none" else ""
            if failure in {"files-error", "hash-error", "files-rate-limit", "hash-rate-limit"}:
                method = provider.compute_diff_files if failure.startswith("files") else provider.compute_diff_hash
                method.side_effect = (
                    ProviderRateLimitError() if failure.endswith("rate-limit") else RuntimeError("git failed")
                )
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"]
            if failure == "missing" and repair_head == "feedbeef"
            else ["fix.py", "keep.py", "followup.py"],
            diff_hash="intentional-followup"
            if repair_head != "feedbeef"
            else ("changed-patch" if failure == "changed" else "preserved"),
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        if repair_head != "feedbeef" and failure.endswith("rate-limit"):
            with pytest.raises(ProviderRateLimitError):
                run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])
            return
        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])
        if failure in {"missing", "changed", "unavailable"} or (repair_head != "feedbeef" and failure):
            assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
            provider.post_comment.assert_not_called()
            if failure == "missing":
                assert "missing intended files" in summary.results[0].details
        else:
            assert summary.results[0].decision == ActionDecision.SKIP
            provider.post_comment.assert_called_once_with(1, "<!-- agdt:conflict-repair-validated:feedbeef -->")

    def test_marker_lookup_rejects_malformed_trusted_comments(self) -> None:
        """Malformed trusted markers are ignored and malformed blockers fail closed."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"

        for body in (
            "not-a-marker",
            "<!-- agdt:conflict-repair:abc123:feedbeef:2026-01-01T00:00:00+00:00 -->",
            "<!-- agdt:conflict-repair:abc123:deadbeef:not-a-time -->",
        ):
            provider.list_issue_comments.return_value = [
                IssueCommentInfo(id=1, author="trusted-bot", body=body),
            ]
            assert _find_recent_conflict_repair_head(provider, 1, "feedbeef") == ""

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=2,
                author="trusted-bot",
                body="not-a-marker",
            ),
        ]
        assert _find_recent_diff_preservation_blocker(provider, 1) is None

        encoded_list = base64.urlsafe_b64encode(json.dumps(["not", "a", "dict"]).encode()).decode().rstrip("=")
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=3,
                author="trusted-bot",
                body=f"<!-- agdt:diff-preservation-blocker:{encoded_list} -->",
            ),
        ]
        with pytest.raises(DiffPreservationBlockerLookupError, match="latest authenticated"):
            _find_recent_diff_preservation_blocker(provider, 1)

    @pytest.mark.parametrize(
        "payload",
        [
            {
                "baseline_head": "",
                "baseline_files": ["fix.py"],
                "baseline_hash": "",
                "baseline_hash_available": True,
                "fingerprint_supported": True,
                "allow_file_removal": False,
                "intentional_noop": False,
            },
            {
                "baseline_head": "head",
                "baseline_files": [""],
                "baseline_hash": "",
                "baseline_hash_available": True,
                "fingerprint_supported": True,
            },
            {
                "baseline_head": "head",
                "baseline_files": ["fix.py"],
                "baseline_hash": None,
                "baseline_hash_available": True,
                "fingerprint_supported": True,
            },
            {
                "baseline_head": "head",
                "baseline_files": ["fix.py"],
                "baseline_hash": "",
                "baseline_hash_available": "yes",
                "fingerprint_supported": True,
            },
            {
                "baseline_head": "head",
                "baseline_files": ["fix.py"],
                "baseline_hash": "",
                "baseline_hash_available": True,
                "fingerprint_supported": "yes",
            },
        ],
    )
    def test_marker_lookup_rejects_invalid_blocker_fields(self, payload: dict[str, object]) -> None:
        """Invalid persisted blocker fields fail closed."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=1, author="trusted-bot", body=_diff_preservation_blocker_comment(payload)),
        ]

        with pytest.raises(DiffPreservationBlockerLookupError, match="latest authenticated"):
            _find_recent_diff_preservation_blocker(provider, 1)

    def test_happy_path_all_skip(self) -> None:
        """All actions skip — no execution."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)
        actions = [
            _MockAction("a", ActionDecision.SKIP),
            _MockAction("b", ActionDecision.SKIP),
        ]
        summary = run_pipeline(provider, snapshot, actions)
        assert len(summary.results) == 2
        assert all(r.decision == ActionDecision.SKIP for r in summary.results)

    def test_persisted_blocker_identity_failure_blocks_pipeline(self) -> None:
        """An unavailable authenticated blocker identity fails closed."""
        provider = MagicMock()
        provider.get_pr_token_login.side_effect = RuntimeError("identity unavailable")
        snapshot = PRStateSnapshot(pr_number=1)

        summary = run_pipeline(provider, snapshot, [_MockAction("publish", ActionDecision.EXECUTE)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "persisted post-mutation diff validation unavailable" in summary.results[0].details

    def test_conflict_repair_identity_failure_blocks_pipeline(self) -> None:
        """An unavailable conflict-repair marker identity fails closed."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner._find_recent_conflict_repair_head",
            side_effect=DiffPreservationBlockerLookupError("identity unavailable"),
        ):
            summary = run_pipeline(provider, snapshot, [_MockAction("approve", ActionDecision.EXECUTE)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "conflict-repair diff validation unavailable" in summary.results[0].details

    def test_guard_block_propagates(self) -> None:
        """When guards BLOCK, subsequent actions are BLOCKED_BY_GUARD."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)
        actions = [
            _MockAction("guards", ActionDecision.BLOCKED),
            _MockAction("publish", ActionDecision.EXECUTE),
            _MockAction("merge", ActionDecision.EXECUTE),
        ]
        summary = run_pipeline(provider, snapshot, actions)
        assert summary.results[0].decision == ActionDecision.BLOCKED
        assert summary.results[1].decision == ActionDecision.BLOCKED_BY_GUARD
        assert summary.results[2].decision == ActionDecision.BLOCKED_BY_GUARD

    def test_execute_action(self) -> None:
        """Action with EXECUTE decision gets execute() called."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)
        actions = [_MockAction("approve", ActionDecision.EXECUTE)]
        summary = run_pipeline(provider, snapshot, actions)
        assert summary.results[0].decision == ActionDecision.EXECUTE
        assert "exec_approve" in summary.results[0].details

    def test_non_guard_blocked_does_not_guard_block_following_actions(self) -> None:
        """Non-guards BLOCKED result should not trigger guard-block behavior."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)
        actions = [
            _MockAction("publish", ActionDecision.BLOCKED),
            _MockAction("merge", ActionDecision.EXECUTE),
        ]

        summary = run_pipeline(provider, snapshot, actions)

        assert summary.results[0].decision == ActionDecision.BLOCKED
        assert summary.results[1].decision == ActionDecision.EXECUTE

    def test_exception_in_evaluation(self) -> None:
        """Exception during evaluate() → FAILED."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)

        class _BrokenAction:
            @property
            def name(self):
                return "broken"

            def evaluate(self, snapshot, derived):
                raise RuntimeError("boom")

            def execute(self, provider, snapshot, derived):
                return ActionResult(name="broken", decision=ActionDecision.EXECUTE)

        actions = [_BrokenAction()]
        summary = run_pipeline(provider, snapshot, actions)
        assert summary.results[0].decision == ActionDecision.FAILED
        assert "boom" in summary.results[0].error

    def test_rate_limit_in_evaluation_is_reraised(self) -> None:
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)
        error = ProviderRateLimitError(provider="github", credential_identity="SPECKIT_PR_TOKEN")

        class _BrokenAction:
            @property
            def name(self):
                return "broken"

            def evaluate(self, snapshot, derived):
                raise error

            def execute(self, provider, snapshot, derived):
                raise AssertionError("execute() should not run")

        with pytest.raises(ProviderRateLimitError):
            run_pipeline(provider, snapshot, [_BrokenAction()])

    def test_exception_in_evaluation_halts_subsequent_execute_actions(self) -> None:
        """Non-guards evaluation failures halt subsequent EXECUTE actions."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)

        class _BrokenAction:
            @property
            def name(self):
                return "request_review"

            def evaluate(self, snapshot, derived):
                raise RuntimeError("boom")

            def execute(self, provider, snapshot, derived):
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

        actions: list[Action] = [_BrokenAction(), _MockAction("merge", ActionDecision.EXECUTE)]
        summary = run_pipeline(provider, snapshot, actions)
        assert summary.results[0].decision == ActionDecision.FAILED
        assert summary.results[1].decision == ActionDecision.SKIP
        assert "request_review" in summary.results[1].details

    def test_failure_gate_skips_evaluate_on_subsequent_actions(self) -> None:
        """exec_failed_by gate fires before evaluate() — subsequent evaluate() not called."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)
        evaluate_called = []

        class _FailingAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.FAILED)

        class _SentinelAction:
            @property
            def name(self):
                return "merge"

            def evaluate(self, snapshot, derived) -> ActionResult:
                evaluate_called.append("merge")
                return ActionResult(name="merge", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="merge", decision=ActionDecision.EXECUTE)

        actions: list[Action] = [_FailingAction(), _SentinelAction()]
        run_pipeline(provider, snapshot, actions)
        assert evaluate_called == [], "evaluate() should not be called on halted action"

    def test_guards_exception_blocks_pipeline(self) -> None:
        """Exception in guards evaluation → BLOCKED, subsequent BLOCKED_BY_GUARD."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)

        class _BrokenGuards:
            @property
            def name(self):
                return "guards"

            def evaluate(self, snapshot, derived):
                raise RuntimeError("guard error")

            def execute(self, provider, snapshot, derived):
                return ActionResult(name="guards", decision=ActionDecision.EXECUTE)

        actions: list[Action] = [_BrokenGuards(), _MockAction("publish", ActionDecision.EXECUTE)]
        summary = run_pipeline(provider, snapshot, actions)
        assert summary.results[0].decision == ActionDecision.BLOCKED
        assert "guard error" in summary.results[0].details
        assert summary.results[1].decision == ActionDecision.BLOCKED_BY_GUARD

    def test_terminating_action_stops_later_actions(self) -> None:
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)

        class _TerminatingAction(_MockAction):
            terminates_run = True

        later = _MockAction("publish", ActionDecision.EXECUTE)
        summary = run_pipeline(
            provider,
            snapshot,
            [_TerminatingAction("retry_failed_session", ActionDecision.EXECUTE), later],
        )
        assert summary.results[0].decision is ActionDecision.EXECUTE
        assert summary.results[1].decision is ActionDecision.SKIP
        assert "terminating action" in summary.results[1].details

    def test_terminating_action_execution_exception_stops_later_actions(self) -> None:
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)

        class _ExplodingTerminatingAction(_MockAction):
            terminates_run = True

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise RuntimeError("retry dispatch failed")

        summary = run_pipeline(
            provider,
            snapshot,
            [
                _ExplodingTerminatingAction("retry_failed_session", ActionDecision.EXECUTE),
                _MockAction("publish", ActionDecision.EXECUTE),
            ],
        )
        assert summary.results[0].decision is ActionDecision.FAILED
        assert summary.results[1].decision is ActionDecision.SKIP

    def test_terminating_action_block_blocks_the_rest_of_pipeline(self) -> None:
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)

        class _TerminatingAction(_MockAction):
            terminates_run = True

        summary = run_pipeline(
            provider,
            snapshot,
            [
                _TerminatingAction("retry_failed_session", ActionDecision.BLOCKED),
                _MockAction("publish", ActionDecision.EXECUTE),
            ],
        )
        assert summary.results[1].decision is ActionDecision.BLOCKED_BY_GUARD

    def test_terminating_action_evaluation_exception_blocks_the_rest(self) -> None:
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)

        class _TerminatingAction:
            terminates_run = True

            @property
            def name(self) -> str:
                return "retry_failed_session"

            def evaluate(self, snapshot, derived) -> ActionResult:
                raise RuntimeError("retry inspection failed")

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("evaluate failure must prevent execution")

        summary = run_pipeline(
            provider,
            snapshot,
            [_TerminatingAction(), _MockAction("publish", ActionDecision.EXECUTE)],
        )
        assert summary.results[0].decision is ActionDecision.FAILED
        assert summary.results[1].decision is ActionDecision.BLOCKED_BY_GUARD

    def test_failed_side_effect_halts_subsequent_executions(self) -> None:
        """When a side-effecting action returns FAILED, subsequent EXECUTE decisions are skipped."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)

        class _FailingAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.FAILED, details="publish failed")

        actions: list[Action] = [
            _FailingAction(),
            _MockAction("approve", ActionDecision.EXECUTE),
            _MockAction("merge", ActionDecision.EXECUTE),
        ]
        summary = run_pipeline(provider, snapshot, actions)
        assert summary.results[0].decision == ActionDecision.FAILED  # publish failed
        assert summary.results[1].decision == ActionDecision.SKIP  # approve halted
        assert "halted" in summary.results[1].details.lower()
        assert "publish" in summary.results[1].details
        assert summary.results[2].decision == ActionDecision.SKIP  # merge halted

    def test_failed_side_effect_exception_halts_subsequent_executions(self) -> None:
        """When a side-effecting action raises during execute(), subsequent EXECUTE decisions are skipped."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)

        class _ExplodingAction:
            @property
            def name(self):
                return "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise RuntimeError("git error")

        actions: list[Action] = [
            _ExplodingAction(),
            _MockAction("merge", ActionDecision.EXECUTE),
        ]
        summary = run_pipeline(provider, snapshot, actions)
        assert summary.results[0].decision == ActionDecision.FAILED
        assert summary.results[1].decision == ActionDecision.SKIP
        assert "halted" in summary.results[1].details.lower()

    def test_rate_limit_in_execution_is_reraised(self) -> None:
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)
        error = ProviderRateLimitError(provider="github", credential_identity="SPECKIT_PR_TOKEN")

        class _ExplodingAction:
            @property
            def name(self):
                return "approve"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="approve", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise error

        with pytest.raises(ProviderRateLimitError):
            run_pipeline(provider, snapshot, [_ExplodingAction()])

    def test_guards_execute_exception_does_not_halt_subsequent_actions(self) -> None:
        """guards execute exception should not set non-guard failure gate."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)

        class _ExplodingGuards:
            @property
            def name(self):
                return "guards"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="guards", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise RuntimeError("guards exploded")

        actions: list[Action] = [_ExplodingGuards(), _MockAction("publish", ActionDecision.EXECUTE)]
        summary = run_pipeline(provider, snapshot, actions)
        assert summary.results[0].decision == ActionDecision.FAILED
        assert summary.results[1].decision == ActionDecision.EXECUTE

    def test_head_changing_action_halts_subsequent_actions_until_rerun(self) -> None:
        """A fresh snapshot is required after an action force-pushes a new HEAD."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)
        evaluate_called = []

        class _HeadChangingAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="publish",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                )

        class _SentinelAction:
            @property
            def name(self):
                return "merge"

            def evaluate(self, snapshot, derived) -> ActionResult:
                evaluate_called.append("merge")
                return ActionResult(name="merge", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="merge", decision=ActionDecision.EXECUTE)

        summary = run_pipeline(provider, snapshot, [_HeadChangingAction(), _SentinelAction()])
        assert summary.results[0].decision == ActionDecision.EXECUTE
        assert summary.results[1].decision == ActionDecision.SKIP
        assert "changed pr head" in summary.results[1].details.lower()
        assert "rerun required" in summary.results[1].details.lower()
        assert evaluate_called == []

    def test_publish_invalidation_marks_squash_and_rebase_as_no_longer_applicable(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Downstream squash/rebase are skipped as no longer applicable after publish invalidates the PR snapshot."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)

        class _PublishAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="publish",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                )

        class _SkippedAction:
            def __init__(self, name: str) -> None:
                self._name = name

            @property
            def name(self):
                return self._name

            def evaluate(self, snapshot, derived) -> ActionResult:
                raise AssertionError("evaluate() should not run after publish invalidates the snapshot")

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("execute() should not run after publish invalidates the snapshot")

        with caplog.at_level(logging.INFO):
            summary = run_pipeline(
                provider,
                snapshot,
                [_PublishAction(), _SkippedAction("squash"), _SkippedAction("rebase")],
            )

        assert summary.results[0].decision == ActionDecision.EXECUTE
        assert summary.results[1].decision == ActionDecision.SKIP
        assert summary.results[2].decision == ActionDecision.SKIP
        assert summary.results[1].details == (
            "No longer applicable after 'publish' in this run: "
            "pre-publish branch preparation invalidated the PR snapshot; rerun required"
        )
        assert summary.results[2].details == summary.results[1].details
        assert "Action 'squash': SKIP (superseded by 'publish' via pre-publish branch preparation" in caplog.text
        assert "Action 'rebase': SKIP (superseded by 'publish' via pre-publish branch preparation" in caplog.text

    @pytest.mark.parametrize(
        ("inventory_outcome", "expected_next_decision", "blocker_remains"),
        [
            ("matching", ActionDecision.EXECUTE, False),
            ("changed", ActionDecision.BLOCKED_BY_GUARD, True),
            ("unavailable", ActionDecision.BLOCKED_BY_GUARD, True),
            ("error", ActionDecision.BLOCKED_BY_GUARD, True),
            ("rate_limit", ActionDecision.BLOCKED_BY_GUARD, True),
            ("unsupported", ActionDecision.BLOCKED_BY_GUARD, True),
        ],
    )
    def test_publish_with_unavailable_fingerprint_revalidates_on_common_base(
        self,
        inventory_outcome: str,
        expected_next_decision: ActionDecision,
        blocker_remains: bool,
    ) -> None:
        """A no-op publish refresh validates its exact inventory against the original base SHA."""
        head_sha = "unchanged-head"
        files = [f"changed/file-{index}.py" for index in range(18)]
        baseline = PRStateSnapshot(
            pr_number=1,
            head_sha=head_sha,
            base_branch="main",
            base_sha="base-before-refresh",
            head_branch="feature",
            commit_count=1,
            title="feat: publish unchanged patch",
            is_draft=True,
            files=files,
            has_changes=True,
            diff_hash="baseline-fingerprint",
            diff_hash_supported=True,
            diff_hash_available=True,
            base_repo_full_name="owner/repo",
        )
        refreshed = PRStateSnapshot(
            pr_number=1,
            head_sha=head_sha,
            base_branch="main",
            base_sha="base-after-refresh",
            head_branch="feature",
            title=baseline.title,
            is_draft=False,
            files=files,
            diff_hash="",
            diff_hash_supported=True,
            diff_hash_available=False,
            base_repo_full_name="owner/repo",
        )
        provider = verified_pr_provider(1, head_sha, files)
        provider.get_pr_token_login.return_value = "trusted-bot"
        issue_comments: list[IssueCommentInfo] = []
        comment_id = 0

        def post_comment(pr_number: int, body: str) -> int:
            nonlocal comment_id
            comment_id += 1
            issue_comments.append(IssueCommentInfo(id=comment_id, author="trusted-bot", body=body))
            return comment_id

        provider.list_issue_comments.side_effect = lambda _pr_number: list(issue_comments)
        provider.post_comment.side_effect = post_comment
        provider.delete_comment.side_effect = lambda id: issue_comments.__setitem__(
            slice(None), [comment for comment in issue_comments if comment.id != id]
        )
        if inventory_outcome == "matching":
            provider.compute_diff_files.return_value = files
        elif inventory_outcome == "changed":
            provider.compute_diff_files.return_value = [*files, "changed/extra.py"]
        elif inventory_outcome == "unavailable":
            provider.compute_diff_files.return_value = None
        elif inventory_outcome == "error":
            provider.compute_diff_files.side_effect = RuntimeError("inventory unavailable")
        elif inventory_outcome == "rate_limit":
            provider.compute_diff_files.side_effect = ProviderRateLimitError(
                provider="github",
                credential_identity="SPECKIT_PR_TOKEN",
            )
        else:
            provider.compute_diff_files = CIPlatformProvider.compute_diff_files.__get__(provider, type(provider))
        pre_publish_head = head_sha
        assert baseline.head_sha == refreshed.head_sha
        assert baseline.base_branch == refreshed.base_branch
        assert baseline.base_sha != refreshed.base_sha
        assert baseline.files == refreshed.files and len(refreshed.files) == 18
        assert refreshed.diff_hash_available is False

        def squash_single_commit_without_changes(**kwargs: str) -> None:
            assert baseline.commit_count == 1
            assert kwargs["head_sha"] == pre_publish_head

        provider.squash_before_publish.side_effect = squash_single_commit_without_changes

        evaluated: list[PRStateSnapshot] = []

        class _NextEligibleAction:
            name = "next"
            runs_after_invalidation = True

            def evaluate(self, snapshot, derived) -> ActionResult:
                evaluated.append(snapshot)
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.publish.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
                return_value=refreshed,
            ),
        ):
            if inventory_outcome == "rate_limit":
                with pytest.raises(ProviderRateLimitError):
                    run_pipeline(provider, baseline, [PublishAction(), _NextEligibleAction()])
                assert evaluated == []
                return
            summary = run_pipeline(provider, baseline, [PublishAction(), _NextEligibleAction()])

        assert provider.squash_before_publish.call_count == 1
        provider.publish_pr.assert_called_once_with(1)
        assert pre_publish_head == refreshed.head_sha
        if inventory_outcome != "unsupported":
            provider.compute_diff_files.assert_called_once_with(
                base_branch="main",
                sha=head_sha,
                base_sha="base-before-refresh",
            )
        assert summary.results[0].decision == ActionDecision.EXECUTE
        assert summary.results[0].invalidates_snapshot is True
        assert summary.results[0].preconditions == {
            "is_draft": True,
            "has_changes": True,
            "not_wip": True,
            "no_active_session": True,
        }
        assert summary.results[1].decision == expected_next_decision
        assert evaluated == ([refreshed] if expected_next_decision == ActionDecision.EXECUTE else [])
        assert (
            any("<!-- agdt:diff-preservation-blocker:" in comment.body for comment in issue_comments) is blocker_remains
        )

    def test_runs_after_invalidation_actions_proceed_after_snapshot_invalidation(self) -> None:
        """Actions with runs_after_invalidation=True execute; others are skipped."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newsha",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        class _InvalidatingAction:
            @property
            def name(self):
                return "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="squash",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        class _OptInAction:
            @property
            def name(self):
                return "resolve_threads"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                assert snapshot.head_sha == "newsha"
                derived.set("opt_in_ran", True)
                return ActionResult(name="resolve_threads", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="resolve_threads", decision=ActionDecision.EXECUTE)

        class _RegularAction:
            @property
            def name(self):
                return "merge"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="merge", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="merge", decision=ActionDecision.EXECUTE)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ) as mock_refresh:
            summary = run_pipeline(provider, snapshot, [_InvalidatingAction(), _OptInAction(), _RegularAction()])

        mock_refresh.assert_called_once_with(provider, 1, actionable_check_names=None)
        assert summary.results[0].decision == ActionDecision.EXECUTE  # squash executed
        assert summary.results[1].decision == ActionDecision.EXECUTE  # resolve_threads proceeded
        assert summary.results[2].decision == ActionDecision.SKIP  # merge halted
        assert "rerun required" in summary.results[2].details.lower()
        assert summary.snapshot is not None
        assert summary.snapshot.head_sha == "newsha"

    @pytest.mark.parametrize("action_type", [ApproveAction, MergeAction])
    def test_refresh_preserves_provider_for_live_head_evaluation(self, action_type):
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "moved-head"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="old-head",
            files=["fix.py"],
            diff_hash="same",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        refreshed = PRStateSnapshot(
            pr_number=1,
            head_sha="refreshed-head",
            files=["fix.py"],
            diff_hash="same",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        invalidating = _MockAction("squash", ActionDecision.EXECUTE)
        invalidating.execute = MagicMock(
            return_value=ActionResult(
                name="squash",
                decision=ActionDecision.EXECUTE,
                invalidates_snapshot=True,
                preserves_diff_fingerprint=True,
            )
        )
        action = action_type()
        action.runs_after_invalidation = True
        with patch("agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot", return_value=refreshed):
            summary = run_pipeline(provider, snapshot, [invalidating, action])
        assert summary.results[1].decision == ActionDecision.SKIP
        assert summary.results[1].preconditions["live_head_matches_snapshot"] is False
        assert "moved-head" in summary.results[1].details
        provider.get_pr_metadata.assert_called_with(1)
        provider.approve_pr.assert_not_called()
        provider.merge_pr.assert_not_called()

    def test_rate_limit_during_refresh_after_invalidation_is_reraised(self) -> None:
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha")
        error = ProviderRateLimitError(provider="github", credential_identity="SPECKIT_PR_TOKEN")

        class _InvalidatingAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE, invalidates_snapshot=True)

        class _OptInAction:
            @property
            def name(self):
                return "resolve_threads"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                raise AssertionError("evaluate() should not run when refresh raises")

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("execute() should not run")

        with patch("agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot", side_effect=error):
            with pytest.raises(ProviderRateLimitError):
                run_pipeline(provider, snapshot, [_InvalidatingAction(), _OptInAction()])

    def test_rate_limit_from_invalidating_action_refreshes_before_reraising(self) -> None:
        """Rate-limit pauses still refresh and validate if the action may have mutated HEAD."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", base_branch="main", files=["fix.py"])
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha", base_branch="main", files=[])

        class _InvalidatingAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                error = ProviderRateLimitError(provider="github", credential_identity="SPECKIT_PR_TOKEN")
                setattr(error, "invalidates_snapshot", True)
                setattr(error, "preserves_diff_fingerprint", True)
                raise error

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ) as mock_refresh:
            with pytest.raises(ProviderRateLimitError):
                run_pipeline(provider, snapshot, [_InvalidatingAction()])

        mock_refresh.assert_called_once_with(provider, 1, actionable_check_names=None)

    @pytest.mark.parametrize(
        "refresh_error",
        [
            RuntimeError("refresh failed"),
            ProviderRateLimitError(provider="github", credential_identity="SPECKIT_PR_TOKEN"),
        ],
    )
    def test_rate_limit_from_invalidating_action_persists_blocker_before_refresh_failure(
        self, refresh_error: Exception
    ) -> None:
        """A rate-limited mutation persists its trusted baseline before refresh can fail."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "oldsha"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            base_branch="main",
            files=["fix.py"],
            diff_hash="pre-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        class _InvalidatingAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                error = ProviderRateLimitError(provider="github", credential_identity="SPECKIT_PR_TOKEN")
                setattr(error, "invalidates_snapshot", True)
                setattr(error, "preserves_diff_fingerprint", True)
                raise error

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            side_effect=refresh_error,
        ) as mock_refresh:
            with pytest.raises(ProviderRateLimitError):
                run_pipeline(provider, snapshot, [_InvalidatingAction()])

        mock_refresh.assert_called_once_with(provider, 1, actionable_check_names=None)
        provider.post_comment.assert_called_once()
        persisted_marker = provider.post_comment.call_args.args[1]
        encoded_payload = persisted_marker.removeprefix("<!-- agdt:diff-preservation-blocker:").removesuffix(" -->")
        persisted_payload = json.loads(zlib.decompress(base64.urlsafe_b64decode(encoded_payload + "==")))
        assert persisted_payload["baseline_head"] == "oldsha"
        assert persisted_payload["baseline_files"] == ["fix.py"]
        assert persisted_payload["baseline_base"] == "main"
        assert persisted_payload["baseline_hash"] == "pre-hash"
        assert persisted_payload["baseline_hash_available"] is True
        assert persisted_payload["fingerprint_supported"] is True

    def test_rate_limit_from_intentional_noop_does_not_persist_blocker(self) -> None:
        """Intentional no-op invalidations stay exempt from persisted blockers on rate limits."""
        provider = MagicMock()
        provider.get_pr_metadata.side_effect = [
            MagicMock(head_sha="oldsha"),
            MagicMock(head_sha="oldsha"),
            MagicMock(head_sha="oldsha"),
        ]
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", base_branch="main")
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha", base_branch="main", files=[])

        class _NoOpAction:
            may_invalidate_snapshot = True

            @property
            def name(self):
                return "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                error = ProviderRateLimitError(provider="github", credential_identity="SPECKIT_PR_TOKEN")
                setattr(error, "invalidates_snapshot", True)
                setattr(error, "intentional_noop", True)
                raise error

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ) as mock_refresh:
            with pytest.raises(ProviderRateLimitError):
                run_pipeline(provider, snapshot, [_NoOpAction()])

        mock_refresh.assert_called_once_with(provider, 1, actionable_check_names=None)
        assert provider.post_comment.call_count == 2
        persisted_marker = provider.post_comment.call_args.args[1]
        encoded_payload = persisted_marker.removeprefix("<!-- agdt:diff-preservation-blocker:").removesuffix(" -->")
        persisted_payload = json.loads(zlib.decompress(base64.urlsafe_b64decode(encoded_payload + "==")))
        assert persisted_payload["intentional_noop"] is True

    def test_skips_oversized_diff_preservation_blocker(self) -> None:
        """An unpostable blocker is skipped instead of exceeding GitHub's comment limit."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "oldsha"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            base_branch="main",
            files=[f"file-{index}-" + hashlib.sha256(str(index).encode()).hexdigest() * 8 for index in range(2000)],
        )

        class _InvalidatingAction:
            name = "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.FAILED,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            side_effect=RuntimeError("refresh failed"),
        ):
            run_pipeline(provider, snapshot, [_InvalidatingAction()])

        provider.post_comment.assert_not_called()

    @pytest.mark.parametrize("downstream_action_name", ["request_review", "approve", "merge"])
    def test_post_mutation_empty_diff_blocks_opt_in_actions(self, downstream_action_name: str) -> None:
        """A mutation that drops the PR diff blocks every downstream opt-in gate."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "oldsha"
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", base_branch="main", files=["fix.py"])
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha", base_branch="main", files=[])

        class _InvalidatingAction:
            name = "rebase"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE, invalidates_snapshot=True)

        class _ReviewAction:
            name = downstream_action_name
            runs_after_invalidation = True

            def evaluate(self, snapshot, derived) -> ActionResult:
                raise AssertionError("empty diff must be blocked before evaluation")

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("empty diff must not be executed")

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            summary = run_pipeline(provider, snapshot, [_InvalidatingAction(), _ReviewAction()])

        assert summary.results[1].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "oldsha" in summary.results[1].details
        assert "newsha" in summary.results[1].details
        assert "fix.py" in summary.results[1].details

    def test_post_mutation_fingerprint_change_blocks_tree_preserving_actions(self) -> None:
        """Tree-preserving invalidations must keep the patch fingerprint stable."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            base_branch="main",
            files=["fix.py"],
            diff_hash="old-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newsha",
            base_branch="main",
            files=["fix.py"],
            diff_hash="new-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        class _InvalidatingAction:
            name = "rebase"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        class _ReviewAction:
            name = "request_review"
            runs_after_invalidation = True

            def evaluate(self, snapshot, derived) -> ActionResult:
                raise AssertionError("fingerprint drift must be blocked before evaluation")

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("fingerprint drift must not be executed")

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            summary = run_pipeline(provider, snapshot, [_InvalidatingAction(), _ReviewAction()])

        assert summary.results[1].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "fingerprint changed" in summary.results[1].details

    def test_post_mutation_identical_snapshot_without_fingerprint_does_not_block(self) -> None:
        """An unchanged HEAD, base, and file set permits downstream actions without a hash."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="same-head",
            base_branch="main",
            base_sha="base-sha-1",
            files=["fix.py", "other.py"],
            diff_hash_supported=True,
            diff_hash_available=False,
        )
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="same-head",
            base_branch="main",
            base_sha="base-sha-1",
            files=["other.py", "fix.py"],
            diff_hash_supported=True,
            diff_hash_available=False,
        )
        seen_heads: list[str] = []

        class _InvalidatingAction:
            name = "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        class _ReviewAction:
            name = "request_review"
            runs_after_invalidation = True

            def evaluate(self, snapshot, derived) -> ActionResult:
                seen_heads.append(snapshot.head_sha)
                return ActionResult(name=self.name, decision=ActionDecision.SKIP)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("a skipped review action must not execute")

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            summary = run_pipeline(provider, snapshot, [_InvalidatingAction(), _ReviewAction()])

        assert seen_heads == ["same-head"]
        assert summary.results[1].decision == ActionDecision.SKIP
        provider.post_comment.assert_not_called()

    def test_post_mutation_fingerprint_change_after_apply_suggestions_allows_opt_in_actions(self) -> None:
        """Patch-changing actions should still be checked for empty/missing files only."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            base_branch="main",
            files=["fix.py"],
            diff_hash="old-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newsha",
            base_branch="main",
            files=["fix.py"],
            diff_hash="new-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        seen_heads: list[str] = []

        class _InvalidatingAction:
            name = "apply_suggestions"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE, invalidates_snapshot=True)

        class _ReviewAction:
            name = "request_review"
            runs_after_invalidation = True

            def evaluate(self, snapshot, derived) -> ActionResult:
                seen_heads.append(snapshot.head_sha)
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            summary = run_pipeline(provider, snapshot, [_InvalidatingAction(), _ReviewAction()])

        assert seen_heads == ["newsha", "newsha"]
        assert summary.results[1].decision == ActionDecision.EXECUTE

    def test_post_mutation_file_removal_after_apply_suggestions_blocks_opt_in_actions(self) -> None:
        """Patch-changing actions cannot remove baseline files without explicit confirmation."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "oldsha"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            base_branch="main",
            files=["fix.py", "keep.py"],
        )
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newsha",
            base_branch="main",
            files=["fix.py"],
        )

        class _InvalidatingAction:
            name = "apply_suggestions"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE, invalidates_snapshot=True)

        class _ReviewAction:
            name = "request_review"
            runs_after_invalidation = True

            def evaluate(self, snapshot, derived) -> ActionResult:
                raise AssertionError("file removal must be blocked before evaluation")

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("file removal must not be executed")

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            summary = run_pipeline(provider, snapshot, [_InvalidatingAction(), _ReviewAction()])

        assert summary.results[1].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "missing files=keep.py" in summary.results[1].details

    def test_post_mutation_explicit_file_removal_authorization_allows_opt_in_actions(self) -> None:
        """An action may explicitly confirm that removing a baseline file is intentional."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "oldsha"
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", base_branch="main", files=["fix.py", "remove.py"])
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha", base_branch="main", files=["fix.py"])

        class _InvalidatingAction:
            name = "apply_suggestions"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                    allows_file_removal=True,
                )

        class _ReviewAction:
            name = "request_review"
            runs_after_invalidation = True

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            summary = run_pipeline(provider, snapshot, [_InvalidatingAction(), _ReviewAction()])

        assert summary.results[1].decision == ActionDecision.EXECUTE
        assert provider.post_comment.call_args_list[-1] == call(
            1,
            _diff_preservation_blocker_comment(
                {
                    "baseline_head": "oldsha",
                    "baseline_base": "main",
                    "baseline_files": ["fix.py", "remove.py"],
                    "baseline_hash": "",
                    "baseline_hash_available": False,
                    "fingerprint_supported": False,
                    "allow_file_removal": True,
                    "allowed_removed_files": [],
                    "intentional_noop": False,
                }
            ),
        )

    def test_post_mutation_empty_to_empty_diff_without_explicit_noop_blocks_opt_in_actions(self) -> None:
        """Invalidations do not infer intentional no-op from empty diffs alone."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            base_branch="main",
            files=[],
            diff_hash="",
            diff_hash_supported=False,
            diff_hash_available=False,
        )
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newsha",
            base_branch="main",
            files=[],
            diff_hash="",
            diff_hash_supported=False,
            diff_hash_available=False,
        )

        class _InvalidatingAction:
            name = "apply_suggestions"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE, invalidates_snapshot=True)

        class _ReviewAction:
            name = "request_review"
            runs_after_invalidation = True

            def evaluate(self, snapshot, derived) -> ActionResult:
                raise AssertionError("implicit empty-to-empty diffs must be blocked before evaluation")

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("implicit empty-to-empty diffs must not be executed")

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            summary = run_pipeline(provider, snapshot, [_InvalidatingAction(), _ReviewAction()])

        assert summary.results[1].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "explicit no-op intent" in summary.results[1].details

    def test_post_mutation_unsupported_fingerprint_does_not_block_when_files_preserved(self) -> None:
        """Fingerprint checks require both action opt-in and provider fingerprint support."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            base_branch="main",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=False,
            diff_hash_available=False,
        )
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newsha",
            base_branch="main",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=False,
            diff_hash_available=False,
        )

        class _InvalidatingAction:
            name = "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        class _ReviewAction:
            name = "request_review"
            runs_after_invalidation = True

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.SKIP)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("request_review should not execute for SKIP result")

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            summary = run_pipeline(provider, snapshot, [_InvalidatingAction(), _ReviewAction()])

        assert summary.results[1].decision == ActionDecision.SKIP

    def test_recent_conflict_repair_marker_with_changed_fingerprint_blocks_pipeline(self) -> None:
        """A repaired head must preserve the pre-repair fingerprint from the dispatch marker."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = "old-hash"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="new-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        actions = [_MockAction("guards", ActionDecision.SKIP)]

        summary = run_pipeline(provider, snapshot, actions)

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "pre-repair HEAD=def456" in summary.results[0].details
        assert "post-repair HEAD=feedbeef" in summary.results[0].details
        assert "fingerprint changed" in summary.results[0].details

    def test_persisted_diff_preservation_blocker_blocks_pipeline_until_diff_restored(self) -> None:
        """A persisted blocker must re-block later runs while the degraded diff remains."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "prehead",
                        "baseline_files": ["fix.py", "keep.py"],
                        "baseline_hash": "same-hash",
                        "baseline_hash_available": True,
                        "fingerprint_supported": True,
                        "allow_file_removal": False,
                        "allowed_removed_files": [],
                        "intentional_noop": False,
                    }
                ),
            )
        ]
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["keep.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "persisted post-mutation diff validation blocked" in summary.results[0].details
        assert "missing files=fix.py" in summary.results[0].details

    def test_valid_persisted_diff_preservation_blocker_is_cleared_after_run(self) -> None:
        """A restored diff clears the persisted blocker once the live HEAD is verified."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "prehead",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "same-hash",
                        "baseline_hash_available": True,
                        "fingerprint_supported": True,
                        "allow_file_removal": False,
                        "allowed_removed_files": [],
                        "intentional_noop": False,
                    }
                ),
            )
        ]
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP
        provider.post_comment.assert_called_once_with(
            1,
            "<!-- agdt:diff-preservation-blocker-cleared:feedbeef -->",
        )

    def test_matching_persisted_blocker_without_fingerprint_is_cleared_safely(self) -> None:
        """A missing-hash blocker clears only after snapshot identity and live HEAD are confirmed."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        blocker = IssueCommentInfo(
            id=10,
            author="trusted-bot",
            body=_diff_preservation_blocker_comment(
                {
                    "baseline_head": "same-head",
                    "baseline_base": "main",
                    "baseline_base_sha": "base-sha-1",
                    "baseline_files": ["fix.py"],
                    "baseline_hash": "",
                    "baseline_hash_available": False,
                    "fingerprint_supported": True,
                    "allow_file_removal": False,
                    "intentional_noop": False,
                }
            ),
        )
        provider.list_issue_comments.return_value = [blocker]
        provider.compute_diff_hash.return_value = None
        provider.get_pr_metadata.return_value.head_sha = "same-head"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="same-head",
            base_branch="main",
            base_sha="base-sha-1",
            files=["fix.py"],
            diff_hash_supported=True,
            diff_hash_available=False,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP
        provider.delete_comment.assert_called_once_with(10)
        provider.post_comment.assert_called_once_with(
            1,
            "<!-- agdt:diff-preservation-blocker-cleared:same-head -->",
        )

    @pytest.mark.parametrize(
        ("baseline_head", "baseline_base", "baseline_files", "current_head", "current_base", "current_files"),
        [
            ("old-head", "main", ["fix.py"], "same-head", "main", ["fix.py"]),
            ("same-head", "release", ["fix.py"], "same-head", "main", ["fix.py"]),
            ("same-head", None, ["fix.py"], "same-head", "main", ["fix.py"]),
            ("same-head", "main", ["fix.py"], "same-head", "main", ["fix.py", "other.py"]),
        ],
    )
    def test_persisted_blocker_without_fingerprint_requires_matching_identity(
        self,
        baseline_head: str,
        baseline_base: str | None,
        baseline_files: list[str],
        current_head: str,
        current_base: str,
        current_files: list[str],
    ) -> None:
        """Mismatched or legacy baseline identity cannot clear a missing-hash blocker."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        payload: dict[str, object] = {
            "baseline_head": baseline_head,
            "baseline_files": baseline_files,
            "baseline_hash": "",
            "baseline_hash_available": False,
            "fingerprint_supported": True,
            "allow_file_removal": False,
            "intentional_noop": False,
        }
        if baseline_base is not None:
            payload["baseline_base"] = baseline_base
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(payload),
            )
        ]
        provider.compute_diff_hash = None
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha=current_head,
            base_branch=current_base,
            files=current_files,
            diff_hash_supported=True,
            diff_hash_available=False,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "fingerprint unavailable" in summary.results[0].details
        provider.delete_comment.assert_not_called()
        provider.post_comment.assert_not_called()

    @patch.dict(os.environ, {"GITHUB_ACTOR": "github-actions[bot]"}, clear=False)
    def test_persist_diff_preservation_blocker_updates_active_summary_comment(self) -> None:
        """When an active summary comment exists, the blocker is embedded in it."""
        provider = MagicMock()
        provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
        provider.get_pr_metadata.return_value.head_sha = "oldsha"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=500,
                author="github-actions[bot]",
                body="<!-- agdt:ai-pr-loop-summary -->\n#### 🤖 AI PR Loop Run\nDetails\n\n🤖 AI PR Loop ·",
            )
        ]
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            base_branch="main",
            files=["fix.py"],
            diff_hash="pre-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        class _InvalidatingAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                error = ProviderRateLimitError(provider="github", credential_identity="SPECKIT_PR_TOKEN")
                setattr(error, "invalidates_snapshot", True)
                setattr(error, "preserves_diff_fingerprint", True)
                raise error

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            side_effect=RuntimeError("refresh failed"),
        ):
            with pytest.raises(ProviderRateLimitError):
                run_pipeline(provider, snapshot, [_InvalidatingAction()])

        provider.update_comment.assert_called_once()
        assert provider.update_comment.call_args.args[0] == 500
        assert "<!-- agdt:diff-preservation-blocker:" in provider.update_comment.call_args.args[1]
        assert provider.update_comment.call_args.args[1].count("🤖 AI PR Loop ·") == 0
        provider.post_comment.assert_not_called()

    @patch.dict(os.environ, {"GITHUB_ACTOR": "github-actions[bot]"}, clear=False)
    def test_persist_diff_preservation_blocker_after_clear_posts_new_comment(self) -> None:
        """A cleared baseline is persisted in a newer comment than the clearing marker."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "github-actions[bot]"
        provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
        provider.get_pr_metadata.return_value.head_sha = "oldsha"
        comments = [
            IssueCommentInfo(
                id=101,
                author="github-actions[bot]",
                body="<!-- agdt:ai-pr-loop-summary -->\n#### 🤖 AI PR Loop Run\nDetails",
            ),
            IssueCommentInfo(
                id=102,
                author="github-actions[bot]",
                body="<!-- agdt:diff-preservation-blocker-cleared:feedbeef -->",
            ),
        ]

        def list_issue_comments(_pr_number: int) -> list[IssueCommentInfo]:
            return list(comments)

        def post_comment(_pr_number: int, body: str) -> int:
            comments.append(IssueCommentInfo(id=103, author="github-actions[bot]", body=body))
            return 103

        provider.list_issue_comments.side_effect = list_issue_comments
        provider.post_comment.side_effect = post_comment
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            base_branch="main",
            files=["fix.py"],
            diff_hash="pre-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        class _InvalidatingAction:
            name = "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                error = ProviderRateLimitError(provider="github", credential_identity="SPECKIT_PR_TOKEN")
                setattr(error, "invalidates_snapshot", True)
                setattr(error, "preserves_diff_fingerprint", True)
                raise error

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
                side_effect=RuntimeError("refresh failed"),
            ),
            pytest.raises(ProviderRateLimitError),
        ):
            run_pipeline(provider, snapshot, [_InvalidatingAction()])

        provider.update_comment.assert_not_called()
        provider.post_comment.assert_called_once()
        assert comments[-1].id > comments[1].id
        assert (
            _find_recent_diff_preservation_blocker(provider, 1)["baseline_head"] == "oldsha"  # type: ignore[index]
        )

    @patch.dict(os.environ, {"GITHUB_ACTOR": "github-actions[bot]"}, clear=False)
    def test_persist_diff_preservation_blocker_replaces_existing_marker_in_summary(self) -> None:
        """When an existing blocker marker is already present in summary, it is replaced."""
        provider = MagicMock()
        provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
        provider.get_pr_metadata.return_value.head_sha = "oldsha"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=500,
                author="github-actions[bot]",
                body=(
                    "<!-- agdt:ai-pr-loop-summary -->\n"
                    "#### 🤖 AI PR Loop Run\n"
                    + _diff_preservation_blocker_comment(
                        {
                            "baseline_head": "oldsha",
                            "baseline_files": ["fix.py"],
                            "baseline_hash": "pre-hash",
                            "baseline_hash_available": True,
                            "fingerprint_supported": True,
                            "allow_file_removal": False,
                            "intentional_noop": False,
                        }
                    )
                ),
            )
        ]
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            base_branch="main",
            files=["fix.py"],
            diff_hash="pre-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        class _InvalidatingAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                error = ProviderRateLimitError(provider="github", credential_identity="SPECKIT_PR_TOKEN")
                setattr(error, "invalidates_snapshot", True)
                setattr(error, "preserves_diff_fingerprint", True)
                raise error

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            side_effect=RuntimeError("refresh failed"),
        ):
            with pytest.raises(ProviderRateLimitError):
                run_pipeline(provider, snapshot, [_InvalidatingAction()])

        provider.update_comment.assert_called_once()
        assert provider.update_comment.call_args.args[0] == 500
        assert "<!-- agdt:diff-preservation-blocker:bm90LWpzb24 -->" not in provider.update_comment.call_args.args[1]

    @patch.dict(os.environ, {"GITHUB_ACTOR": "trusted-bot"}, clear=False)
    def test_clear_diff_preservation_blocker_strips_summary_and_deletes_standalone(self, monkeypatch) -> None:
        """Clearing removes the blocker from summary and deletes legacy standalone comments."""
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.get_bookkeeping_token_login.return_value = "trusted-bot"
        blocker_body = _diff_preservation_blocker_comment(
            {
                "baseline_head": "prehead",
                "baseline_files": ["fix.py"],
                "baseline_hash": "same-hash",
                "baseline_hash_available": True,
                "fingerprint_supported": True,
                "allow_file_removal": False,
                "allowed_removed_files": [],
                "intentional_noop": False,
            }
        )
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=500,
                author="trusted-bot",
                body=f"<!-- agdt:ai-pr-loop-summary -->\n#### 🤖 AI PR Loop Run\n{blocker_body}",
            ),
            IssueCommentInfo(
                id=501,
                author="trusted-bot",
                body=blocker_body,
            ),
            IssueCommentInfo(
                id=502,
                author="someone-else",
                body=blocker_body,
            ),
        ]
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP
        provider.update_comment.assert_called_once()
        assert "<!-- agdt:diff-preservation-blocker:" not in provider.update_comment.call_args.args[1]
        provider.delete_comment.assert_called_once_with(501)

    @patch.dict(os.environ, {"GITHUB_ACTOR": "trusted-bot"}, clear=False)
    def test_clear_diff_preservation_blocker_deletes_labeled_standalone_comment(self, monkeypatch) -> None:
        """Cleanup recognizes the exact terminal label on a standalone blocker."""
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.get_bookkeeping_token_login.return_value = "trusted-bot"
        blocker_body = _diff_preservation_blocker_comment(
            {
                "baseline_head": "prehead",
                "baseline_files": ["fix.py"],
                "baseline_hash": "same-hash",
                "baseline_hash_available": True,
                "fingerprint_supported": True,
                "allow_file_removal": False,
                "allowed_removed_files": [],
                "intentional_noop": False,
            }
        )
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=501, author="trusted-bot", body=f"{blocker_body}\n\n🤖 AI PR Loop ·"),
        ]
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        provider.delete_comment.assert_called_once_with(501)

    @patch.dict(os.environ, {"GITHUB_ACTOR": "trusted-bot"}, clear=False)
    def test_clear_summary_blocker_tombstones_residual_legacy_standalone_comment(self, monkeypatch) -> None:
        """A summary clear tombstone supersedes a preserved PAT-authored standalone blocker."""
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        provider = MagicMock()
        provider.get_trusted_loop_comment_logins.return_value = {"trusted-bot", "legacy-pat"}
        provider.get_pr_token_login.return_value = "legacy-pat"
        provider.get_bookkeeping_token_login.return_value = "trusted-bot"
        blocker_body = _diff_preservation_blocker_comment(
            {
                "baseline_head": "prehead",
                "baseline_files": ["fix.py"],
                "baseline_hash": "same-hash",
                "baseline_hash_available": True,
                "fingerprint_supported": True,
                "allow_file_removal": False,
                "allowed_removed_files": [],
                "intentional_noop": False,
            }
        )
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=500,
                author="trusted-bot",
                body=f"<!-- agdt:ai-pr-loop-summary -->\n#### 🤖 AI PR Loop Run\n{blocker_body}",
            ),
            IssueCommentInfo(id=501, author="legacy-pat", body=blocker_body),
        ]
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        provider.update_comment.assert_called_once()
        provider.delete_comment.assert_not_called()
        provider.post_comment.assert_called_once_with(1, "<!-- agdt:diff-preservation-blocker-cleared:feedbeef -->")

    @patch.dict(os.environ, {"GITHUB_ACTOR": "trusted-bot"}, clear=False)
    def test_clear_summary_blocker_without_residual_standalone_state_needs_no_tombstone(self, monkeypatch) -> None:
        """A cleared summary needs no tombstone after all standalone state is absent."""
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.get_bookkeeping_token_login.return_value = "trusted-bot"
        blocker_body = _diff_preservation_blocker_comment(
            {
                "baseline_head": "prehead",
                "baseline_files": ["fix.py"],
                "baseline_hash": "same-hash",
                "baseline_hash_available": True,
                "fingerprint_supported": True,
                "allow_file_removal": False,
                "allowed_removed_files": [],
                "intentional_noop": False,
            }
        )
        summary_comments = [
            IssueCommentInfo(
                id=500,
                author="trusted-bot",
                body=f"<!-- agdt:ai-pr-loop-summary -->\n#### 🤖 AI PR Loop Run\n{blocker_body}",
            ),
        ]
        provider.list_issue_comments.return_value = summary_comments

        def update_summary(comment_id: int, body: str) -> None:
            summary_comments[0] = IssueCommentInfo(
                id=comment_id,
                author="trusted-bot",
                body=body,
            )

        provider.update_comment.side_effect = update_summary
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        provider.update_comment.assert_called_once()
        provider.delete_comment.assert_not_called()
        provider.post_comment.assert_not_called()

    @patch.dict(os.environ, {"GITHUB_ACTOR": "trusted-bot"}, clear=False)
    def test_clear_migrated_summary_tombstones_embedded_residual_blocker(self, monkeypatch) -> None:
        """A cleaned bot copy cannot hide the embedded blocker in the older PAT summary."""
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        provider = MagicMock()
        provider.get_trusted_loop_comment_logins.return_value = {"trusted-bot", "legacy-pat"}
        provider.get_pr_token_login.return_value = "legacy-pat"
        provider.get_bookkeeping_token_login.return_value = "trusted-bot"
        blocker_body = _diff_preservation_blocker_comment(
            {
                "baseline_head": "prehead",
                "baseline_files": ["fix.py"],
                "baseline_hash": "same-hash",
                "baseline_hash_available": True,
                "fingerprint_supported": True,
                "allow_file_removal": False,
                "allowed_removed_files": [],
                "intentional_noop": False,
            }
        )
        comments = [
            IssueCommentInfo(
                id=500,
                author="legacy-pat",
                body=f"<!-- agdt:ai-pr-loop-summary -->\n#### 🤖 AI PR Loop Run\n{blocker_body}",
            ),
        ]
        provider.list_issue_comments.return_value = comments

        def migrate_summary(comment_id: int, body: str) -> None:
            comments.append(
                IssueCommentInfo(
                    id=501,
                    author="trusted-bot",
                    body=f"{body}\n\n🤖 AI PR Loop ·",
                )
            )

        provider.update_comment.side_effect = migrate_summary
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        provider.update_comment.assert_called_once()
        provider.post_comment.assert_called_once_with(1, "<!-- agdt:diff-preservation-blocker-cleared:feedbeef -->")

    @patch.dict(os.environ, {"GITHUB_ACTOR": "trusted-bot"}, clear=False)
    def test_clear_diff_preservation_blocker_skips_standalone_cleanup_without_trusted_login(self, monkeypatch) -> None:
        """Standalone cleanup is skipped when the trusted login cannot be resolved."""
        monkeypatch.setenv("GITHUB_ACTIONS", "true")

        class _Provider(SimpleNamespace):
            def __init__(self) -> None:
                super().__init__(
                    list_issue_comments=MagicMock(),
                    get_bookkeeping_token_login=None,
                    get_trusted_loop_comment_logins=MagicMock(return_value={"trusted-bot"}),
                    get_pr_metadata=MagicMock(),
                    update_comment=MagicMock(),
                    delete_comment=MagicMock(),
                    post_comment=MagicMock(),
                )
                self._login_lookups = 0

            @property
            def get_pr_token_login(self):  # type: ignore[override]
                self._login_lookups += 1
                if self._login_lookups == 1:
                    return lambda: "trusted-bot"
                return None

        provider = _Provider()
        provider.list_issue_comments = MagicMock()
        provider.get_pr_metadata = MagicMock()
        provider.update_comment = MagicMock()
        provider.delete_comment = MagicMock()
        provider.post_comment = MagicMock()
        blocker_body = _diff_preservation_blocker_comment(
            {
                "baseline_head": "prehead",
                "baseline_files": ["fix.py"],
                "baseline_hash": "same-hash",
                "baseline_hash_available": True,
                "fingerprint_supported": True,
                "allow_file_removal": False,
                "allowed_removed_files": [],
                "intentional_noop": False,
            }
        )
        provider.list_issue_comments.return_value = [IssueCommentInfo(id=501, author="trusted-bot", body=blocker_body)]
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        run_pipeline(cast(CIPlatformProvider, provider), snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        provider.delete_comment.assert_not_called()

    @patch.dict(os.environ, {"GITHUB_ACTOR": "trusted-bot"}, clear=False)
    def test_clear_diff_preservation_blocker_logs_and_skips_when_trusted_login_lookup_fails(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Trusted-login lookup failures do not delete standalone comments."""
        provider = MagicMock()
        login_calls = 0

        def _login_lookup() -> str:
            nonlocal login_calls
            login_calls += 1
            if login_calls == 1:
                return "trusted-bot"
            raise RuntimeError("lookup failed")

        provider.get_pr_token_login.side_effect = _login_lookup
        blocker_body = _diff_preservation_blocker_comment(
            {
                "baseline_head": "prehead",
                "baseline_files": ["fix.py"],
                "baseline_hash": "same-hash",
                "baseline_hash_available": True,
                "fingerprint_supported": True,
                "allow_file_removal": False,
                "allowed_removed_files": [],
                "intentional_noop": False,
            }
        )
        provider.list_issue_comments.return_value = [IssueCommentInfo(id=501, author="trusted-bot", body=blocker_body)]
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        provider.delete_comment.assert_not_called()
        provider.update_comment.assert_not_called()
        last_login_lookup = max(i for i, call in enumerate(provider.mock_calls) if call[0] == "get_pr_token_login")
        assert all(call[0] != "list_issue_comments" for call in provider.mock_calls[last_login_lookup + 1 :])
        provider.post_comment.assert_called_once_with(1, "<!-- agdt:diff-preservation-blocker-cleared:feedbeef -->")
        assert "comment identity lookup failed" in caplog.text

    @patch.dict(os.environ, {"GITHUB_ACTOR": "trusted-bot"}, clear=False)
    @pytest.mark.parametrize("unusable_login", [123, "   "])
    def test_clear_diff_preservation_blocker_skips_standalone_cleanup_for_unusable_trusted_login(
        self, unusable_login: int | str
    ) -> None:
        """Unusable trusted-login results do not authorize standalone cleanup."""
        provider = MagicMock()
        login_calls = 0

        def _login_lookup() -> str | int:
            nonlocal login_calls
            login_calls += 1
            if login_calls == 1:
                return "trusted-bot"
            return unusable_login

        provider.get_pr_token_login.side_effect = _login_lookup
        blocker_body = _diff_preservation_blocker_comment(
            {
                "baseline_head": "prehead",
                "baseline_files": ["fix.py"],
                "baseline_hash": "same-hash",
                "baseline_hash_available": True,
                "fingerprint_supported": True,
                "allow_file_removal": False,
                "allowed_removed_files": [],
                "intentional_noop": False,
            }
        )
        provider.list_issue_comments.return_value = [IssueCommentInfo(id=501, author="trusted-bot", body=blocker_body)]
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        provider.delete_comment.assert_not_called()
        provider.update_comment.assert_not_called()
        last_login_lookup = max(i for i, call in enumerate(provider.mock_calls) if call[0] == "get_pr_token_login")
        assert all(call[0] != "list_issue_comments" for call in provider.mock_calls[last_login_lookup + 1 :])
        provider.post_comment.assert_called_once_with(1, "<!-- agdt:diff-preservation-blocker-cleared:feedbeef -->")

    @patch.dict(os.environ, {"GITHUB_ACTOR": "trusted-bot"}, clear=False)
    def test_clear_diff_preservation_blocker_tombstones_after_login_rate_limit(self) -> None:
        """A trusted-login rate limit skips comment cleanup but still posts a tombstone."""
        provider = MagicMock()
        login_calls = 0

        def _login_lookup() -> str:
            nonlocal login_calls
            login_calls += 1
            if login_calls == 1:
                return "trusted-bot"
            raise ProviderRateLimitError(provider="github", credential_identity="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT")

        provider.get_pr_token_login.side_effect = _login_lookup
        blocker_body = _diff_preservation_blocker_comment(
            {
                "baseline_head": "prehead",
                "baseline_files": ["fix.py"],
                "baseline_hash": "same-hash",
                "baseline_hash_available": True,
                "fingerprint_supported": True,
                "allow_file_removal": False,
                "allowed_removed_files": [],
                "intentional_noop": False,
            }
        )
        provider.list_issue_comments.return_value = [IssueCommentInfo(id=501, author="trusted-bot", body=blocker_body)]
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        provider.update_comment.assert_not_called()
        last_login_lookup = max(i for i, call in enumerate(provider.mock_calls) if call[0] == "get_pr_token_login")
        assert all(call[0] != "list_issue_comments" for call in provider.mock_calls[last_login_lookup + 1 :])
        provider.post_comment.assert_called_once_with(1, "<!-- agdt:diff-preservation-blocker-cleared:feedbeef -->")

    @patch.dict(os.environ, {"GITHUB_ACTOR": "trusted-bot"}, clear=False)
    def test_clear_diff_preservation_blocker_tombstones_when_login_unresolved(self) -> None:
        """Unauthenticated cleanup leaves comments untouched and posts a tombstone."""
        provider = MagicMock()
        login_calls = 0

        def _login_lookup() -> str:
            nonlocal login_calls
            login_calls += 1
            if login_calls == 1:
                return "trusted-bot"
            raise RuntimeError("lookup failed")

        provider.get_pr_token_login.side_effect = _login_lookup
        blocker_body = _diff_preservation_blocker_comment(
            {
                "baseline_head": "prehead",
                "baseline_files": ["fix.py"],
                "baseline_hash": "same-hash",
                "baseline_hash_available": True,
                "fingerprint_supported": True,
                "allow_file_removal": False,
                "allowed_removed_files": [],
                "intentional_noop": False,
            }
        )
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=500,
                author="trusted-bot",
                body=f"<!-- agdt:ai-pr-loop-summary -->\n#### 🤖 AI PR Loop Run\n{blocker_body}",
            ),
            IssueCommentInfo(id=501, author="trusted-bot", body=blocker_body),
        ]
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        provider.update_comment.assert_not_called()
        last_login_lookup = max(i for i, call in enumerate(provider.mock_calls) if call[0] == "get_pr_token_login")
        assert all(call[0] != "list_issue_comments" for call in provider.mock_calls[last_login_lookup + 1 :])
        provider.delete_comment.assert_not_called()
        provider.post_comment.assert_called_once_with(1, "<!-- agdt:diff-preservation-blocker-cleared:feedbeef -->")

    def test_definitive_no_mutation_clears_blocker_after_concurrent_push(self) -> None:
        """A rejected mutation does not block a later concurrent HEAD."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = []
        provider.get_pr_metadata.side_effect = [
            MagicMock(head_sha="feedbeef"),
            MagicMock(head_sha="concurrent"),
        ]
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        action = _MockAction(
            "rebase",
            ActionDecision.EXECUTE,
            ActionDecision.FAILED,
            definitive_no_mutation=True,
            may_invalidate_snapshot=True,
        )

        summary = run_pipeline(provider, snapshot, [action])

        assert summary.results[0].decision == ActionDecision.FAILED
        assert provider.post_comment.call_args_list[1].args == (
            1,
            "<!-- agdt:diff-preservation-blocker-cleared:concurrent -->",
        )

    @pytest.mark.parametrize("name", ["publish", "dispatch_conflict_resolution"])
    def test_final_eligibility_skip_clears_baseline_after_concurrent_push(self, name):
        """A skipped mutation must not attribute another writer's push to its baseline."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = []
        provider.get_pr_metadata.side_effect = [
            MagicMock(head_sha="feedbeef"),
            MagicMock(head_sha="concurrent"),
        ]
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        action = MagicMock()
        action.name = name
        action.may_invalidate_snapshot = name == "publish"
        action.evaluate.side_effect = [
            ActionResult(name, ActionDecision.EXECUTE),
            ActionResult(name, ActionDecision.SKIP, details="Concurrent writer moved HEAD"),
        ]

        summary = run_pipeline(provider, snapshot, [action])

        assert summary.results[0].decision == ActionDecision.SKIP
        action.execute.assert_not_called()
        assert provider.post_comment.call_args_list[1].args == (
            1,
            "<!-- agdt:diff-preservation-blocker-cleared:concurrent -->",
        )

    def test_pending_persisted_conflict_repair_blocker_is_not_cleared(self) -> None:
        """A conflict-repair blocker remains armed while the repair agent has not pushed."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "feedbeef",
                        "baseline_base": "main",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "same-hash",
                        "baseline_hash_available": True,
                        "fingerprint_supported": True,
                        "allow_file_removal": False,
                        "intentional_noop": False,
                        "conflict_repair": True,
                    }
                ),
            )
        ]
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP
        provider.post_comment.assert_not_called()

    def test_valid_persisted_diff_preservation_blocker_recomputes_missing_baseline_hash(self) -> None:
        """A persisted blocker can recover once the baseline fingerprint becomes available again."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "prehead",
                        "baseline_base": "base-at-dispatch",
                        "baseline_base_sha": "base-sha-1",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "",
                        "baseline_hash_available": False,
                        "fingerprint_supported": True,
                    }
                ),
            )
        ]
        provider.compute_diff_hash.return_value = "same-hash"
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="base-sha-1",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP
        provider.compute_diff_hash.assert_called_once_with(
            base_branch="base-at-dispatch",
            sha="prehead",
            base_sha="base-sha-1",
        )
        provider.post_comment.assert_called_once_with(
            1,
            "<!-- agdt:diff-preservation-blocker-cleared:feedbeef -->",
        )

    def test_valid_persisted_diff_preservation_blocker_without_hash_lookup_stays_blocked(self) -> None:
        """Without hash lookup capability, a missing persisted baseline fingerprint still fails closed."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "prehead",
                        "baseline_base": "main",
                        "baseline_base_sha": "base-sha-1",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "",
                        "baseline_hash_available": False,
                        "fingerprint_supported": True,
                    }
                ),
            )
        ]
        provider.compute_diff_hash = None
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="base-sha-1",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "fingerprint unavailable" in summary.results[0].details

    def test_persisted_diff_preservation_blocker_without_base_sha_does_not_recompute_hash(self) -> None:
        """Legacy blockers without a pinned base cannot recover a hash against a mutable ref."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "prehead",
                        "baseline_base": "main",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "",
                        "baseline_hash_available": False,
                        "fingerprint_supported": True,
                    }
                ),
            )
        ]
        provider.compute_diff_hash.return_value = "same-hash"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="prehead",
            base_branch="main",
            base_sha="base-sha-2",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "fingerprint unavailable" in summary.results[0].details
        provider.compute_diff_hash.assert_not_called()

    def test_valid_persisted_diff_preservation_blocker_logs_empty_recomputed_hash(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """An empty recomputed persisted baseline fingerprint remains unavailable and is logged."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "prehead",
                        "baseline_base": "main",
                        "baseline_base_sha": "base-sha-1",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "",
                        "baseline_hash_available": False,
                        "fingerprint_supported": True,
                    }
                ),
            )
        ]
        provider.compute_diff_hash.return_value = ""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="base-sha-1",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "fingerprint unavailable" in summary.results[0].details
        assert "Ignoring empty persisted baseline fingerprint" in caplog.text

    def test_valid_persisted_diff_preservation_blocker_with_non_string_recomputed_hash_stays_blocked(self) -> None:
        """A non-string recomputed persisted baseline fingerprint is treated as unavailable."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "prehead",
                        "baseline_base": "main",
                        "baseline_base_sha": "base-sha-1",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "",
                        "baseline_hash_available": False,
                        "fingerprint_supported": True,
                    }
                ),
            )
        ]
        provider.compute_diff_hash.return_value = None
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="base-sha-1",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "fingerprint unavailable" in summary.results[0].details

    def test_valid_persisted_diff_preservation_blocker_logs_recompute_failure(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A persisted baseline hash lookup failure logs and remains fail-closed."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "prehead",
                        "baseline_base": "main",
                        "baseline_base_sha": "base-sha-1",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "",
                        "baseline_hash_available": False,
                        "fingerprint_supported": True,
                    }
                ),
            )
        ]
        provider.compute_diff_hash.side_effect = RuntimeError("git failure")
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="base-sha-1",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "fingerprint unavailable" in summary.results[0].details
        assert "Failed to recompute persisted baseline fingerprint" in caplog.text

    def test_valid_persisted_diff_preservation_blocker_reraises_rate_limit_during_recompute(self) -> None:
        """Rate limits while recomputing a persisted baseline fingerprint must propagate."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "prehead",
                        "baseline_base": "main",
                        "baseline_base_sha": "base-sha-1",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "",
                        "baseline_hash_available": False,
                        "fingerprint_supported": True,
                    }
                ),
            )
        ]
        provider.compute_diff_hash.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
        )
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="base-sha-1",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        with pytest.raises(ProviderRateLimitError):
            run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

    def test_valid_persisted_diff_preservation_blocker_logs_when_clear_fails(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A non-rate-limit clear failure logs and leaves the run otherwise successful."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "prehead",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "same-hash",
                        "baseline_hash_available": True,
                        "fingerprint_supported": True,
                    }
                ),
            )
        ]
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        provider.post_comment.side_effect = RuntimeError("comment failed")
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP
        assert "Failed to clear diff-preservation blocker" in caplog.text

    def test_valid_persisted_diff_preservation_blocker_reraises_rate_limit_during_clear(self) -> None:
        """Rate limits while clearing a blocker must propagate."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "prehead",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "same-hash",
                        "baseline_hash_available": True,
                        "fingerprint_supported": True,
                    }
                ),
            )
        ]
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        provider.post_comment.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
        )
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        with pytest.raises(ProviderRateLimitError):
            run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

    def test_valid_persisted_diff_preservation_blocker_skips_clear_when_live_head_missing(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A missing live HEAD must skip clearing the blocker."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "prehead",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "same-hash",
                        "baseline_hash_available": True,
                        "fingerprint_supported": True,
                    }
                ),
            )
        ]
        provider.get_pr_metadata.return_value.head_sha = ""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP
        provider.post_comment.assert_not_called()
        assert "live HEAD could not be confirmed" in caplog.text

    def test_valid_persisted_diff_preservation_blocker_skips_clear_for_stale_head(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A stale live HEAD must not clear a blocker for another commit."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "prehead",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "same-hash",
                        "baseline_hash_available": True,
                        "fingerprint_supported": True,
                    }
                ),
            )
        ]
        provider.get_pr_metadata.return_value.head_sha = "otherhead"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP
        provider.post_comment.assert_not_called()
        assert "Skipping diff-preservation blocker clear for stale HEAD" in caplog.text

    def test_valid_persisted_diff_preservation_blocker_logs_when_live_head_lookup_fails(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A non-rate-limit live HEAD lookup failure logs and skips clearing."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "prehead",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "same-hash",
                        "baseline_hash_available": True,
                        "fingerprint_supported": True,
                    }
                ),
            )
        ]
        provider.get_pr_metadata.side_effect = RuntimeError("metadata failed")
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP
        provider.post_comment.assert_not_called()
        assert "Failed to verify live HEAD before clearing diff-preservation blocker" in caplog.text

    def test_valid_persisted_diff_preservation_blocker_reraises_rate_limit_during_live_head_lookup(self) -> None:
        """Rate limits while verifying live HEAD for blocker clearing must propagate."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "prehead",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "same-hash",
                        "baseline_hash_available": True,
                        "fingerprint_supported": True,
                    }
                ),
            )
        ]
        provider.get_pr_metadata.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
        )
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        with pytest.raises(ProviderRateLimitError):
            run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

    def test_recent_conflict_repair_marker_reports_missing_baseline_files(self) -> None:
        """Cross-run validation should report dropped files from pre-repair file inventory."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash = None
        provider.compute_diff_files.return_value = ["fix.py", "keep.py"]
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["keep.py"],
            diff_hash="",
            diff_hash_supported=False,
            diff_hash_available=False,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "missing files=fix.py" in summary.results[0].details
        assert "<pre-repair-diff>" not in summary.results[0].details

    def test_recent_conflict_repair_marker_without_file_inventory_capability_blocks_without_fingerprint(self) -> None:
        """Providers without a trusted baseline inventory fail closed when fingerprinting is unavailable."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash = None
        provider.compute_diff_files = None
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=False,
            diff_hash_available=False,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "pre-repair file inventory unavailable" in summary.results[0].details
        assert "changed-file count=1" in summary.results[0].details
        assert "missing files=<unavailable>" in summary.results[0].details

    def test_recent_conflict_repair_marker_without_file_inventory_capability_uses_hash_fallback(self) -> None:
        """Live files are only an acceptable fallback when matching fingerprints authenticate the diff."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = "same-hash"
        provider.compute_diff_files = None
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP

    def test_recent_conflict_repair_marker_file_inventory_failure_logs_and_blocks_without_fingerprint(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """A non-rate-limit file-inventory failure logs and fails closed without fingerprint data."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash = None
        provider.compute_diff_files.side_effect = RuntimeError("inventory failed")
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=False,
            diff_hash_available=False,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "pre-repair file inventory unavailable" in summary.results[0].details
        assert "Failed to compute pre-repair file inventory" in caplog.text

    def test_recent_conflict_repair_marker_file_inventory_rate_limit_is_reraised(self) -> None:
        """Rate limits while loading pre-repair file inventory must propagate."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash = None
        provider.compute_diff_files.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
        )
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=False,
            diff_hash_available=False,
        )

        with pytest.raises(ProviderRateLimitError):
            run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

    def test_recent_conflict_repair_marker_with_matching_fingerprint_allows_pipeline(self) -> None:
        """Cross-run validation should allow downstream actions when fingerprint matches."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = "same-hash"
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP
        provider.post_comment.assert_called_once_with(
            1,
            "<!-- agdt:conflict-repair-validated:feedbeef -->",
        )

    def test_newer_validated_marker_for_different_head_consumes_dispatch(self) -> None:
        """A newer validation marker consumes the older dispatch by comment ordering."""
        provider = MagicMock()
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.get_trusted_loop_comment_logins.return_value = {"trusted-bot", "github-actions[bot]"}
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:deadbeef:{marker_time} -->",
            ),
            IssueCommentInfo(
                id=11,
                author="trusted-bot",
                body="<!-- agdt:conflict-repair-validated:abcdef12 -->",
            ),
        ]

        assert _find_recent_conflict_repair_head(provider, 1, "12345678") == ""

    def test_recent_conflict_repair_marker_without_fingerprint_support_blocks_without_inventory(self) -> None:
        """Without fingerprinting, recent repairs need a recovered pre-repair file inventory."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash = None
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=False,
            diff_hash_available=False,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "pre-repair file inventory unavailable" in summary.results[0].details

    def test_cross_run_validation_logs_and_continues_when_validation_marker_persistence_fails(self) -> None:
        """A persistence failure should not bypass validation or fail a valid repaired head."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.find_comment.side_effect = [
            None,
            (1, f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->"),
            None,
        ]
        provider.compute_diff_hash.return_value = "same-hash"
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        provider.post_comment.side_effect = RuntimeError("comment failed")
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP

    def test_cross_run_validation_reraises_rate_limit_during_validation_marker_persistence(self) -> None:
        """Rate limits while persisting the consumed baseline must propagate."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = "same-hash"
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        provider.post_comment.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
        )
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        with pytest.raises(ProviderRateLimitError):
            run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

    def test_recent_conflict_repair_marker_with_unavailable_pre_hash_blocks_pipeline(self) -> None:
        """A capable provider returning None for the baseline fingerprint fails closed."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = None
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=True,
            diff_hash_available=False,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "pre-repair file inventory unavailable" in summary.results[0].details

    def test_cross_run_repair_uses_matching_exact_diffs_when_fingerprints_are_unavailable(self) -> None:
        """Matching complete diffs against one pinned base validate an otherwise un-fingerprinted repair."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = None
        provider.compute_diff_files.return_value = ["fix.py"]
        exact_diff = "diff --git a/fix.py b/fix.py\n--- a/fix.py\n+++ b/fix.py\n@@ -1 +1 @@\n-old\n+new\n"
        provider.get_commit_range_diff_bytes.side_effect = [exact_diff.encode(), exact_diff.encode()]
        provider.get_commit_range_diff_change_counts.return_value = {"fix.py": 2}
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=True,
            diff_hash_available=False,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP
        assert provider.get_commit_range_diff_bytes.call_args_list == [
            call("pinned-base", "def456"),
            call("pinned-base", "feedbeef"),
        ]
        provider.post_comment.assert_called_once_with(
            1,
            "<!-- agdt:conflict-repair-validated:feedbeef -->",
        )

    def test_cross_run_repair_blocks_changed_exact_diff_with_same_file_inventory(self) -> None:
        """Equal file inventories do not authorize a repair with different patch content."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = None
        provider.compute_diff_files.return_value = ["fix.py"]
        provider.get_commit_range_diff_bytes.side_effect = [
            b"diff --git a/fix.py b/fix.py\n@@ -1 +1 @@\n-old\n+first\n",
            b"diff --git a/fix.py b/fix.py\n@@ -1 +1 @@\n-old\n+different\n",
        ]
        provider.get_commit_range_diff_change_counts.return_value = {"fix.py": 2}
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=True,
            diff_hash_available=False,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "fingerprint changed" in summary.results[0].details
        provider.post_comment.assert_not_called()

    def test_cross_run_repair_blocks_dropped_file_with_exact_diff_fallback(self) -> None:
        """Exact diff evidence cannot override a removed pre-repair file."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = None
        provider.compute_diff_files.return_value = ["fix.py", "keep.py"]
        provider.get_commit_range_diff_bytes.side_effect = [
            b"diff --git a/fix.py b/fix.py\n@@ -1 +1 @@\n-old\n+new\n",
            b"diff --git a/keep.py b/keep.py\n@@ -1 +1 @@\n-old\n+new\n",
            b"diff --git a/fix.py b/fix.py\n@@ -1 +1 @@\n-old\n+new\n",
        ]
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=True,
            diff_hash_available=False,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "missing files=keep.py" in summary.results[0].details
        provider.post_comment.assert_not_called()

    @pytest.mark.parametrize("failure_mode", ["none", "error", "unsupported"])
    def test_cross_run_repair_blocks_when_exact_diff_evidence_is_unavailable(self, failure_mode: str) -> None:
        """Unavailable pinned-base comparisons leave the repair marker outstanding."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = None
        provider.compute_diff_files.return_value = ["fix.py"]
        if failure_mode == "none":
            provider.get_commit_range_diff_bytes.return_value = None
        elif failure_mode == "error":
            provider.get_commit_range_diff_bytes.side_effect = RuntimeError("comparison unavailable")
        else:
            provider.get_commit_range_diff_bytes = None
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=True,
            diff_hash_available=False,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "fingerprint unavailable" in summary.results[0].details
        provider.post_comment.assert_not_called()

    @pytest.mark.parametrize(
        ("exact_diff", "change_count"),
        [
            ("diff --git a/other.py b/other.py\n@@ -1 +1 @@\n-old\n+new\n", 2),
            ("diff --git a/fix.py b/fix.py\nBinary files a/fix.py and b/fix.py differ\n", 0),
        ],
        ids=("missing-inventory-file", "opaque-binary-diff"),
    )
    def test_cross_run_repair_rejects_incomplete_exact_diff_evidence(self, exact_diff: str, change_count: int) -> None:
        """Incomplete inventories and opaque binary diffs cannot validate a repair."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = None
        provider.compute_diff_files.return_value = ["fix.py"]
        provider.get_commit_range_diff_bytes.return_value = exact_diff.encode()
        provider.get_commit_range_diff_change_counts.return_value = {"fix.py": change_count}
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=True,
            diff_hash_available=False,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "fingerprint unavailable" in summary.results[0].details
        provider.post_comment.assert_not_called()

    def test_cross_run_repair_rejects_truncated_hunk_with_matching_file_header(self) -> None:
        """Matching diff headers cannot make a patch with incomplete hunk counts trustworthy."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = None
        provider.compute_diff_files.return_value = ["fix.py"]
        truncated_diff = "diff --git a/fix.py b/fix.py\n@@ -1,2 +1,2 @@\n-old\n+new\n"
        provider.get_commit_range_diff_bytes.return_value = truncated_diff.encode()
        provider.get_commit_range_diff_change_counts.return_value = {"fix.py": 2}
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=True,
            diff_hash_available=False,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "fingerprint unavailable" in summary.results[0].details
        provider.post_comment.assert_not_called()

    @pytest.mark.parametrize(
        ("exact_diff", "inventory"),
        [
            (
                "diff --git a/old.py b/new.py\n"
                "similarity index 50%\n"
                "rename from old.py\n"
                "rename to new.py\n"
                "@@ -1 +1 @@\n-old\n+new\n",
                "new.py",
            ),
            (
                'diff --git "a/caf\\303\\251.py" "b/caf\\303\\251.py"\n@@ -1 +1 @@\n-old\n+new\n',
                "café.py",
            ),
        ],
        ids=("rename-destination", "octal-escaped-path"),
    )
    def test_cross_run_repair_accepts_complete_rename_aware_exact_diffs(self, exact_diff: str, inventory: str) -> None:
        """Complete exact patches match destination inventories after decoding Git path quoting."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = None
        provider.compute_diff_files.return_value = [inventory]
        provider.get_commit_range_diff_bytes.return_value = exact_diff.encode()
        provider.get_commit_range_diff_change_counts.return_value = {inventory: 2}
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=[inventory],
            diff_hash="",
            diff_hash_supported=True,
            diff_hash_available=False,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP
        assert provider.get_commit_range_diff_bytes.call_args_list == [
            call("pinned-base", "def456"),
            call("pinned-base", "feedbeef"),
        ]
        provider.post_comment.assert_called_once_with(
            1,
            "<!-- agdt:conflict-repair-validated:feedbeef -->",
        )

    def test_persisted_conflict_repair_fallback_validates_dispatch_against_pinned_diffs(self) -> None:
        """A normal repair dispatch can be validated on the next run using exact pinned-base diffs."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        provider.list_issue_comments.return_value = []
        provider.compute_diff_hash.return_value = None
        exact_diff = b"diff --git a/fix.py b/fix.py\n@@ -1 +1 @@\n-old\n+new\n"
        provider.get_commit_range_diff_bytes.side_effect = [exact_diff, exact_diff]
        provider.get_commit_range_diff_change_counts.return_value = {"fix.py": 2}
        dispatch_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=True,
            diff_hash_available=False,
        )

        class _DispatchConflictResolutionAction:
            name = "dispatch_conflict_resolution"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

        dispatched = run_pipeline(provider, dispatch_snapshot, [_DispatchConflictResolutionAction()])
        assert dispatched.results[0].decision == ActionDecision.EXECUTE
        persisted_blocker = provider.post_comment.call_args.args[1]
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=persisted_blocker,
            )
        ]
        provider.get_pr_metadata.return_value.head_sha = "newhead"
        repaired_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newhead",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=True,
            diff_hash_available=False,
        )

        repaired = run_pipeline(provider, repaired_snapshot, [_MockAction("approve", ActionDecision.SKIP)])

        assert repaired.results[0].decision == ActionDecision.SKIP
        assert provider.get_commit_range_diff_bytes.call_args_list == [
            call("pinned-base", "feedbeef"),
            call("pinned-base", "newhead"),
        ]
        assert provider.post_comment.call_args_list[-2:] == [
            call(1, "<!-- agdt:conflict-repair-validated:newhead -->"),
            call(1, "<!-- agdt:diff-preservation-blocker-cleared:newhead -->"),
        ]

    def test_persisted_conflict_repair_fallback_requires_the_original_pinned_base(self) -> None:
        """Persisted repair comparisons cannot use a base different from the dispatched baseline."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "oldhead",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "",
                        "baseline_hash_available": False,
                        "fingerprint_supported": True,
                        "allow_file_removal": False,
                        "intentional_noop": False,
                        "conflict_repair": True,
                        "baseline_base": "main",
                        "baseline_base_sha": "original-base",
                    }
                ),
            )
        ]
        provider.compute_diff_hash.return_value = None
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newhead",
            base_branch="main",
            base_sha="advanced-base",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=True,
            diff_hash_available=False,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("approve", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "fingerprint unavailable" in summary.results[0].details
        provider.get_commit_range_diff_bytes.assert_not_called()
        provider.post_comment.assert_not_called()

    def test_persisted_conflict_repair_fallback_rejects_truncated_diff(self) -> None:
        """A matching but truncated persisted-baseline patch cannot validate a repair."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "oldhead",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "",
                        "baseline_hash_available": False,
                        "fingerprint_supported": True,
                        "allow_file_removal": False,
                        "intentional_noop": False,
                        "conflict_repair": True,
                        "baseline_base": "main",
                        "baseline_base_sha": "pinned-base",
                    }
                ),
            )
        ]
        provider.compute_diff_hash.return_value = None
        truncated_diff = "diff --git a/fix.py b/fix.py\n@@ -1,2 +1,2 @@\n-old\n+new\n"
        provider.get_commit_range_diff_bytes.return_value = truncated_diff.encode()
        provider.get_commit_range_diff_change_counts.return_value = {"fix.py": 2}
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newhead",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=True,
            diff_hash_available=False,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("approve", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "fingerprint unavailable" in summary.results[0].details
        provider.get_commit_range_diff_bytes.assert_has_calls(
            [
                call("pinned-base", "oldhead"),
                call("pinned-base", "newhead"),
            ]
        )
        provider.post_comment.assert_not_called()

    def test_cross_run_repair_reraises_rate_limit_during_exact_diff_comparison(self) -> None:
        """Rate limits from the pinned-base fallback propagate to the pipeline caller."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = None
        provider.compute_diff_files.return_value = ["fix.py"]
        provider.get_commit_range_diff_bytes.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
        )
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="",
            diff_hash_supported=True,
            diff_hash_available=False,
        )

        with pytest.raises(ProviderRateLimitError):
            run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        provider.post_comment.assert_not_called()

    def test_cross_run_repair_blocks_matching_hashes_without_a_pinned_base(self) -> None:
        """Matching hashes computed against an unpinned moving base are not sufficient evidence."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = "same-hash"
        provider.compute_diff_files.return_value = ["fix.py"]
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "fingerprint unavailable" in summary.results[0].details
        provider.post_comment.assert_not_called()

    def test_recent_conflict_repair_marker_with_empty_pre_hash_blocks_pipeline(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """An empty baseline fingerprint string is treated as unavailable and logged."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = ""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="current-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "pre-repair file inventory unavailable" in summary.results[0].details
        assert "Ignoring empty pre-repair fingerprint" in caplog.text

    def test_cross_run_validation_persists_the_final_verified_head(self) -> None:
        """A validated repair marker is recorded only after the final refreshed HEAD is verified."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        provider.get_pr_metadata.side_effect = [
            MagicMock(head_sha="feedbeef"),
            MagicMock(head_sha="finalhead"),
            MagicMock(head_sha="finalhead"),
        ]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = "same-hash"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="finalhead",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        class _InvalidatingAction:
            name = "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        class _ReviewAction:
            name = "request_review"
            runs_after_invalidation = True

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.SKIP)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("request_review should not execute for SKIP result")

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            provider.get_pr_metadata.return_value.head_sha = "finalhead"
            summary = run_pipeline(provider, snapshot, [_InvalidatingAction(), _ReviewAction()])

        assert summary.results[1].decision == ActionDecision.SKIP
        assert provider.post_comment.call_args_list == [
            call(
                1,
                _diff_preservation_blocker_comment(
                    {
                        "baseline_head": "feedbeef",
                        "baseline_base": "main",
                        "baseline_base_sha": "pinned-base",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "same-hash",
                        "baseline_hash_available": True,
                        "fingerprint_supported": True,
                        "allow_file_removal": False,
                        "allowed_removed_files": [],
                        "intentional_noop": False,
                    }
                ),
            ),
            call(1, "<!-- agdt:conflict-repair-validated:finalhead -->"),
            call(1, "<!-- agdt:diff-preservation-blocker-cleared:finalhead -->"),
        ]

    def test_cross_run_validation_does_not_persist_when_later_refresh_fails(self) -> None:
        """A later invalidation without a verified refreshed HEAD must not consume the baseline."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = "same-hash"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        class _InvalidatingAction:
            name = "rebase"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE, invalidates_snapshot=True)

        class _OptInAction:
            name = "request_review"
            runs_after_invalidation = True

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("request_review should not execute when refresh fails")

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            side_effect=RuntimeError("refresh failed"),
        ):
            summary = run_pipeline(provider, snapshot, [_InvalidatingAction(), _OptInAction()])

        assert summary.results[1].decision == ActionDecision.FAILED
        provider.post_comment.assert_called_once_with(
            1,
            _diff_preservation_blocker_comment(
                {
                    "baseline_head": "feedbeef",
                    "baseline_base": "main",
                    "baseline_base_sha": "pinned-base",
                    "baseline_files": ["fix.py"],
                    "baseline_hash": "same-hash",
                    "baseline_hash_available": True,
                    "fingerprint_supported": False,
                    "allow_file_removal": False,
                    "allowed_removed_files": [],
                    "intentional_noop": False,
                }
            ),
        )

    def test_cross_run_validation_does_not_persist_after_new_repair_dispatch(self) -> None:
        """A newly dispatched repair must keep the older validated baseline unconsumed."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = "same-hash"
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            base_sha="pinned-base",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        class _DispatchConflictResolutionAction:
            name = "dispatch_conflict_resolution"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                derived.set("repair_dispatched", True)
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

        summary = run_pipeline(provider, snapshot, [_DispatchConflictResolutionAction()])

        assert summary.results[0].decision == ActionDecision.EXECUTE
        provider.post_comment.assert_called_once()
        encoded_payload = (
            provider.post_comment.call_args.args[1]
            .removeprefix("<!-- agdt:diff-preservation-blocker:")
            .removesuffix(" -->")
        )
        persisted_payload = json.loads(zlib.decompress(base64.urlsafe_b64decode(encoded_payload + "==")))
        assert persisted_payload["conflict_repair"] is True

    def test_conflict_repair_dispatch_persists_pre_dispatch_baseline(self) -> None:
        """A conflict-repair dispatch records the exact diff before handing off the PR."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        provider.list_issue_comments.return_value = []
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        class _DispatchConflictResolutionAction:
            name = "dispatch_conflict_resolution"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

        summary = run_pipeline(provider, snapshot, [_DispatchConflictResolutionAction()])

        assert summary.results[0].decision == ActionDecision.EXECUTE
        provider.post_comment.assert_called_once()
        encoded_payload = (
            provider.post_comment.call_args.args[1]
            .removeprefix("<!-- agdt:diff-preservation-blocker:")
            .removesuffix(" -->")
        )
        persisted_payload = json.loads(zlib.decompress(base64.urlsafe_b64decode(encoded_payload + "==")))
        assert persisted_payload == {
            "baseline_base": "main",
            "baseline_base_sha": "",
            "baseline_files": ["fix.py"],
            "baseline_hash": "same-hash",
            "baseline_hash_available": True,
            "baseline_head": "feedbeef",
            "conflict_repair": True,
            "fingerprint_supported": True,
            "intentional_noop": False,
            "allow_file_removal": False,
            "allowed_removed_files": [],
        }

    def test_persisted_conflict_repair_baseline_blocks_dropped_diff(self) -> None:
        """A dropped file is blocked from downstream actions without refetching the old HEAD."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "oldhead",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "same-hash",
                        "baseline_hash_available": True,
                        "fingerprint_supported": True,
                        "allow_file_removal": False,
                        "intentional_noop": False,
                        "conflict_repair": True,
                    }
                ),
            )
        ]
        provider.compute_diff_hash.side_effect = AssertionError("old HEAD should not be refetched")
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newhead",
            base_branch="main",
            files=[],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("approve", ActionDecision.EXECUTE)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "missing files=fix.py" in summary.results[0].details
        provider.compute_diff_hash.assert_not_called()

    def test_persisted_conflict_repair_baseline_allows_preserved_diff(self) -> None:
        """A preserved diff consumes its stored baseline without refetching the old HEAD."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.get_pr_metadata.return_value.head_sha = "newhead"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "oldhead",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "same-hash",
                        "baseline_hash_available": True,
                        "fingerprint_supported": True,
                        "allow_file_removal": False,
                        "intentional_noop": False,
                        "conflict_repair": True,
                    }
                ),
            )
        ]
        provider.compute_diff_hash.side_effect = AssertionError("old HEAD should not be refetched")
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newhead",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("approve", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP
        assert provider.compute_diff_hash.call_count == 0
        assert provider.post_comment.call_args_list == [
            call(1, "<!-- agdt:conflict-repair-validated:newhead -->"),
            call(1, "<!-- agdt:diff-preservation-blocker-cleared:newhead -->"),
        ]

    def test_failed_conflict_repair_validation_persistence_keeps_blocker(self) -> None:
        """A failed validation marker post keeps the cross-run blocker armed."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.get_pr_metadata.return_value.head_sha = "newhead"
        provider.post_comment.side_effect = RuntimeError("post failed")
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=_diff_preservation_blocker_comment(
                    {
                        "baseline_head": "oldhead",
                        "baseline_files": ["fix.py"],
                        "baseline_hash": "same-hash",
                        "baseline_hash_available": True,
                        "fingerprint_supported": True,
                        "allow_file_removal": False,
                        "intentional_noop": False,
                        "conflict_repair": True,
                    }
                ),
            )
        ]
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newhead",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("approve", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP
        provider.post_comment.assert_called_once_with(
            1,
            "<!-- agdt:conflict-repair-validated:newhead -->",
        )

    def test_conflict_repair_dispatch_requires_persisted_baseline(self) -> None:
        """A dispatch is blocked when its pre-mutation baseline cannot be persisted."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.get_pr_metadata.return_value.head_sha = ""
        provider.list_issue_comments.return_value = []
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
        )

        class _DispatchConflictResolutionAction:
            name = "dispatch_conflict_resolution"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("dispatch must not run without a persisted baseline")

        summary = run_pipeline(provider, snapshot, [_DispatchConflictResolutionAction()])

        assert summary.results[0].decision == ActionDecision.FAILED
        assert "pre-dispatch baseline" in summary.results[0].details

    def test_recent_conflict_repair_marker_with_non_string_pre_hash_blocks_pipeline(self) -> None:
        """A non-string pre-repair fingerprint is treated as unavailable and blocked."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.return_value = object()
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "pre-repair file inventory unavailable" in summary.results[0].details

    def test_recent_conflict_repair_marker_with_pre_hash_lookup_error_blocks_pipeline(self) -> None:
        """A failed pre-repair fingerprint lookup fails closed for recent conflict repairs."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.side_effect = RuntimeError("git failure")
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "pre-repair file inventory unavailable" in summary.results[0].details

    def test_recent_conflict_repair_marker_rate_limit_error_is_reraised(self) -> None:
        """Rate limits during cross-run baseline hashing are propagated."""
        provider = MagicMock()
        provider.list_pr_commits.return_value = [{"sha": "def456"}, {"sha": "feedbeef"}]
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"

        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]
        provider.compute_diff_hash.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
            is_rate_limit=True,
        )
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="feedbeef",
            base_branch="main",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        with pytest.raises(ProviderRateLimitError):
            run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

    def test_second_invalidation_uses_latest_pre_mutation_head_in_diagnostic(self) -> None:
        """Diagnostics must use the head that existed right before the failing mutation."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1, head_sha="initial", base_branch="main", files=["fix.py"])
        first_refresh = PRStateSnapshot(pr_number=1, head_sha="midsha", base_branch="main", files=["fix.py"])
        second_refresh = PRStateSnapshot(pr_number=1, head_sha="finalsha", base_branch="main", files=[])

        class _FirstInvalidatingAction:
            name = "apply_suggestions"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE, invalidates_snapshot=True)

        class _SecondInvalidatingOptInAction:
            name = "dispatch_repair"
            runs_after_invalidation = True

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name=self.name, decision=ActionDecision.EXECUTE, invalidates_snapshot=True)

        class _LaterOptInAction:
            name = "request_review"
            runs_after_invalidation = True

            def evaluate(self, snapshot, derived) -> ActionResult:
                raise AssertionError("guard should block before evaluate")

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("guard should block before execute")

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            side_effect=[first_refresh, second_refresh],
        ):
            summary = run_pipeline(
                provider,
                snapshot,
                [_FirstInvalidatingAction(), _SecondInvalidatingOptInAction(), _LaterOptInAction()],
            )

        assert summary.results[2].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "pre-mutation HEAD=midsha" in summary.results[2].details
        assert "pre-mutation HEAD=initial" not in summary.results[2].details
        assert "post-mutation HEAD=finalsha" in summary.results[2].details

    def test_runs_after_invalidation_actions_share_refreshed_derived_state(self) -> None:
        """All opt-in actions after invalidation share refreshed snapshot/derived state."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newsha",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        observed: list[str] = []

        class _InvalidatingAction:
            @property
            def name(self):
                return "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="squash",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        class _FirstOptInAction:
            @property
            def name(self):
                return "resolve_threads"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                observed.append(snapshot.head_sha)
                derived.set("marker", "set-by-first-optin")
                return ActionResult(name="resolve_threads", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="resolve_threads", decision=ActionDecision.EXECUTE)

        class _SecondOptInAction:
            @property
            def name(self):
                return "request_review"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                observed.append(snapshot.head_sha)
                assert derived.marker == "set-by-first-optin"
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ) as mock_refresh:
            summary = run_pipeline(
                provider,
                snapshot,
                [_InvalidatingAction(), _FirstOptInAction(), _SecondOptInAction()],
            )

        mock_refresh.assert_called_once_with(provider, 1, actionable_check_names=None)
        assert observed == ["newsha", "newsha", "newsha", "newsha"]
        assert [r.decision for r in summary.results] == [
            ActionDecision.EXECUTE,
            ActionDecision.EXECUTE,
            ActionDecision.EXECUTE,
        ]

    def test_runs_after_invalidation_preserves_exclusion_context(self) -> None:
        """Exclusion context from pre-refresh derived state is carried into refreshed state."""
        from agentic_devtools.cli.ci.pipeline.exclusion import ExclusionContext

        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", files=["fix.py"])
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha", files=["fix.py"])
        exclusion_context = ExclusionContext(resolved_comment_ids={101, 102})

        class _InvalidatingAction:
            @property
            def name(self):
                return "apply_suggestions"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="apply_suggestions", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                derived.set("exclusion_context", exclusion_context)
                return ActionResult(
                    name="apply_suggestions",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                )

        class _OptInAction:
            @property
            def name(self):
                return "dispatch_repair"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                assert snapshot.head_sha == "newsha"
                assert derived.get("exclusion_context") == exclusion_context
                return ActionResult(name="dispatch_repair", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="dispatch_repair", decision=ActionDecision.EXECUTE)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ) as mock_refresh:
            summary = run_pipeline(provider, snapshot, [_InvalidatingAction(), _OptInAction()])

        mock_refresh.assert_called_once_with(provider, 1, actionable_check_names=None)
        assert [r.decision for r in summary.results] == [
            ActionDecision.EXECUTE,
            ActionDecision.EXECUTE,
        ]

    def test_runs_after_invalidation_refresh_uses_same_actionable_check_names(self) -> None:
        """The post-invalidation refresh reuses the run's actionable_check_names."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha")
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha")
        actionable_check_names = frozenset({"custom-check", "another-check"})

        class _InvalidatingAction:
            @property
            def name(self):
                return "apply_suggestions"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="apply_suggestions", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="apply_suggestions",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                )

        class _OptInAction:
            @property
            def name(self):
                return "resolve_threads"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="resolve_threads", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="resolve_threads", decision=ActionDecision.EXECUTE)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ) as mock_refresh:
            run_pipeline(
                provider,
                snapshot,
                [_InvalidatingAction(), _OptInAction()],
                actionable_check_names=actionable_check_names,
            )

        mock_refresh.assert_called_once_with(provider, 1, actionable_check_names=actionable_check_names)

    def test_runs_after_invalidation_preserves_autofix_applied_flag(self) -> None:
        """autofix_applied_this_iteration survives the post-invalidation refresh."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", files=["fix.py"])
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha", files=["fix.py"])
        observed: list[object] = []

        class _InvalidatingAction:
            @property
            def name(self):
                return "apply_suggestions"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="apply_suggestions", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                derived.set("autofix_applied_this_iteration", True)
                return ActionResult(
                    name="apply_suggestions",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                )

        class _OptInAction:
            @property
            def name(self):
                return "resolve_threads"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                observed.append(derived.get("autofix_applied_this_iteration", False))
                return ActionResult(name="resolve_threads", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="resolve_threads", decision=ActionDecision.EXECUTE)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            run_pipeline(provider, snapshot, [_InvalidatingAction(), _OptInAction()])

        assert observed == [True, True]

    def test_runs_after_invalidation_without_autofix_flag_defaults_false(self) -> None:
        """The autofix flag is not fabricated when the invalidating action never set it."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newsha",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        observed: list[object] = []

        class _InvalidatingAction:
            @property
            def name(self):
                return "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="squash",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        class _OptInAction:
            @property
            def name(self):
                return "resolve_threads"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                observed.append(derived.get("autofix_applied_this_iteration", False))
                return ActionResult(name="resolve_threads", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="resolve_threads", decision=ActionDecision.EXECUTE)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            run_pipeline(provider, snapshot, [_InvalidatingAction(), _OptInAction()])

        assert observed == [False, False]

    def test_runs_after_invalidation_preserves_squash_preserved_green(self) -> None:
        """squash_preserved_green is carried when refreshed head_sha matches the post-squash SHA."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newsha",
            ci_status="pending",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        class _InvalidatingAction:
            @property
            def name(self):
                return "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                derived.set("squash_preserved_green", True)
                derived.set("squash_preserved_green_sha", "newsha")
                return ActionResult(
                    name="squash",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        class _OptInAction:
            @property
            def name(self):
                return "request_review"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                assert snapshot.head_sha == "newsha"
                assert derived.get("squash_preserved_green") is True
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ) as mock_refresh:
            summary = run_pipeline(provider, snapshot, [_InvalidatingAction(), _OptInAction()])

        mock_refresh.assert_called_once_with(provider, 1, actionable_check_names=None)
        assert [r.decision for r in summary.results] == [
            ActionDecision.EXECUTE,
            ActionDecision.EXECUTE,
        ]

    def test_runs_after_invalidation_drops_squash_flag_on_sha_mismatch(self) -> None:
        """squash_preserved_green is withheld when the refreshed head_sha differs from the post-squash SHA.

        A concurrent push after squash_post_repair but before the snapshot refresh moves the
        PR to a different HEAD. The mismatch causes the flag to be withheld so that
        RequestReviewAction fails closed and defers to fresh CI.
        """
        provider = MagicMock()
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        # A concurrent push moved the branch to "concurrentsha" — not the post-squash "squashedsha"
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="concurrentsha",
            ci_status="pending",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        class _InvalidatingAction:
            @property
            def name(self):
                return "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                derived.set("squash_preserved_green", True)
                derived.set("squash_preserved_green_sha", "squashedsha")
                return ActionResult(
                    name="squash",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        class _OptInAction:
            @property
            def name(self):
                return "request_review"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                # SHA mismatch: flag must not be present
                assert derived.get("squash_preserved_green", False) is False
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            summary = run_pipeline(provider, snapshot, [_InvalidatingAction(), _OptInAction()])

        assert [r.decision for r in summary.results] == [
            ActionDecision.EXECUTE,
            ActionDecision.EXECUTE,
        ]

    def test_runs_after_invalidation_without_squash_flag_defaults_false(self) -> None:
        """When squash did not set the flag, it is not carried into the refreshed state."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newsha",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        class _InvalidatingAction:
            @property
            def name(self):
                return "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="squash",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        class _OptInAction:
            @property
            def name(self):
                return "request_review"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                assert derived.get("squash_preserved_green", False) is False
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ) as mock_refresh:
            summary = run_pipeline(provider, snapshot, [_InvalidatingAction(), _OptInAction()])

        mock_refresh.assert_called_once_with(provider, 1, actionable_check_names=None)
        assert [r.decision for r in summary.results] == [
            ActionDecision.EXECUTE,
            ActionDecision.EXECUTE,
        ]

    def test_runs_after_invalidation_recomputes_unresolved_threads_without_stale_override(self) -> None:
        """The post-invalidation refresh recomputes unresolved_threads from a fresh query.

        ``resolve_threads`` sets an ``unresolved_threads`` derived override for the
        pre-squash snapshot. That override is intentionally dropped by the refresh:
        the rebuilt snapshot re-queries the provider (whose thread-signals cache is
        invalidated after the resolve mutations), so downstream opt-in actions see
        the true post-resolution count rather than the stale pre-refresh override.
        """
        provider = MagicMock()
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            unresolved_threads=7,
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        # Fresh query after resolution + squash: all threads are resolved.
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newsha",
            unresolved_threads=0,
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        observed: list[int] = []

        class _ResolveThreadsAction:
            @property
            def name(self):
                return "resolve_threads"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="resolve_threads", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                # Mirrors ResolveThreadsAction: derived override for this run only.
                derived.set("unresolved_threads", 7)
                return ActionResult(name="resolve_threads", decision=ActionDecision.EXECUTE)

        class _InvalidatingAction:
            @property
            def name(self):
                return "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="squash",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        class _OptInAction:
            @property
            def name(self):
                return "request_review"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                observed.append(derived.unresolved_threads)
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ) as mock_refresh:
            summary = run_pipeline(
                provider,
                snapshot,
                [_ResolveThreadsAction(), _InvalidatingAction(), _OptInAction()],
            )

        mock_refresh.assert_called_once_with(provider, 1, actionable_check_names=None)
        # The stale pre-refresh override (7) must not survive the refresh.
        assert observed == [0, 0]
        assert [r.decision for r in summary.results] == [
            ActionDecision.EXECUTE,
            ActionDecision.EXECUTE,
            ActionDecision.EXECUTE,
        ]

    def test_summary_derived_unresolved_threads_reflects_derived_override(self) -> None:
        """The summary records the derived count the gates read, not the snapshot count."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", unresolved_threads=1)

        class _ResolveThreadsAction:
            @property
            def name(self):
                return "resolve_threads"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="resolve_threads", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                derived.set("unresolved_threads", 71)
                return ActionResult(name="resolve_threads", decision=ActionDecision.EXECUTE)

        summary = run_pipeline(provider, snapshot, [_ResolveThreadsAction()])

        assert summary.snapshot is not None
        assert summary.snapshot.unresolved_threads == 1
        assert summary.derived_unresolved_threads == 71

    def test_summary_derived_unresolved_threads_populated_post_refresh(self) -> None:
        """After a post-invalidation refresh the summary carries the rebuilt derived count."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", unresolved_threads=7)
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha", unresolved_threads=3)

        class _InvalidatingAction:
            @property
            def name(self):
                return "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                derived.set("unresolved_threads", 7)
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE, invalidates_snapshot=True)

        class _OptInAction:
            @property
            def name(self):
                return "request_review"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            summary = run_pipeline(provider, snapshot, [_InvalidatingAction(), _OptInAction()])

        assert summary.derived_unresolved_threads == 3

    def test_runs_after_invalidation_fails_when_snapshot_refresh_raises(self) -> None:
        """Refresh failures on opt-in actions fail closed and halt remaining actions."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "oldsha"
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha")

        class _InvalidatingAction:
            @property
            def name(self):
                return "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE, invalidates_snapshot=True)

        class _OptInAction:
            @property
            def name(self):
                return "resolve_threads"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="resolve_threads", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="resolve_threads", decision=ActionDecision.EXECUTE)

        class _FollowingAction:
            @property
            def name(self):
                return "request_review"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            side_effect=RuntimeError("refresh failed"),
        ) as mock_refresh:
            summary = run_pipeline(
                provider,
                snapshot,
                [_InvalidatingAction(), _OptInAction(), _FollowingAction()],
            )

        mock_refresh.assert_called_once_with(provider, 1, actionable_check_names=None)
        assert summary.results[0].decision == ActionDecision.EXECUTE
        assert summary.results[1].decision == ActionDecision.FAILED
        assert "Failed to refresh snapshot" in summary.results[1].details
        assert summary.results[2].decision == ActionDecision.SKIP
        assert "halted" in summary.results[2].details.lower()
        persisted_marker = provider.post_comment.call_args.args[1]
        assert persisted_marker.startswith("<!-- agdt:diff-preservation-blocker:")

    def test_failed_invalidating_action_refreshes_immediately_and_blocks_dropped_diff(self) -> None:
        """A failed mutating action still refreshes and validates the pushed HEAD."""
        provider = MagicMock()
        provider.get_pr_metadata.side_effect = [
            MagicMock(head_sha="oldsha"),
            MagicMock(head_sha="newsha"),
        ]
        provider.post_comment.side_effect = [RuntimeError("comment failed"), None]
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            base_branch="main",
            files=["fix.py"],
        )
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newsha",
            base_branch="main",
            files=[],
        )

        class _PartialFailureAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="publish",
                    decision=ActionDecision.FAILED,
                    details="publish_pr failed",
                    error="publish failed",
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        class _LaterAction:
            @property
            def name(self):
                return "merge"

            def evaluate(self, snapshot, derived) -> ActionResult:
                raise AssertionError("evaluate() should not run after invalid diff validation fails")

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("execute() should not run after invalid diff validation fails")

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ) as mock_refresh:
            summary = run_pipeline(provider, snapshot, [_PartialFailureAction(), _LaterAction()])

        mock_refresh.assert_called_once_with(provider, 1, actionable_check_names=None)
        assert summary.snapshot is refreshed_snapshot
        assert summary.results[0].decision == ActionDecision.FAILED
        assert summary.results[1].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "post-mutation diff validation blocked" in summary.results[1].details
        assert provider.post_comment.call_count == 1
        persisted_marker = provider.post_comment.call_args.args[1]
        assert persisted_marker.startswith("<!-- agdt:diff-preservation-blocker:")

    def test_intentional_noop_invalidation_refreshes_without_persisting_blocker(self) -> None:
        """Explicit no-op invalidations refresh downstream state without arming a blocker."""
        provider = MagicMock()
        provider.get_pr_metadata.side_effect = [MagicMock(head_sha="oldsha"), MagicMock(head_sha="newsha")]
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            base_branch="main",
        )
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newsha",
            base_branch="main",
            files=[],
        )

        class _NoOpAction:
            may_invalidate_snapshot = True

            @property
            def name(self):
                return "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="squash",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                    intentional_noop=True,
                )

        class _OptInAction:
            @property
            def name(self):
                return "request_review"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                assert snapshot is refreshed_snapshot
                return ActionResult(name="request_review", decision=ActionDecision.SKIP)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("request_review should not execute for SKIP result")

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ) as mock_refresh:
            summary = run_pipeline(provider, snapshot, [_NoOpAction(), _OptInAction()])

        mock_refresh.assert_called_once_with(provider, 1, actionable_check_names=None)
        assert summary.results[0].decision == ActionDecision.EXECUTE
        assert summary.results[1].decision == ActionDecision.SKIP
        assert provider.post_comment.call_count == 2
        marker = provider.post_comment.call_args.args[1]
        assert marker.startswith("<!-- agdt:diff-preservation-blocker:")
        payload = json.loads(
            zlib.decompress(
                base64.urlsafe_b64decode(
                    marker.removeprefix("<!-- agdt:diff-preservation-blocker:").removesuffix(" -->") + "==="
                )
            )
        )
        assert payload["intentional_noop"] is True

    def test_mutating_action_is_skipped_when_blocker_persistence_fails(self, caplog: pytest.LogCaptureFixture) -> None:
        """A mutating action does not execute when its baseline cannot be persisted."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "oldsha"
        provider.post_comment.side_effect = RuntimeError("comment failed")
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", base_branch="main", files=["fix.py"])
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha", base_branch="main", files=[])

        class _PartialFailureAction:
            may_invalidate_snapshot = True
            preserves_diff_fingerprint = True

            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("execute() must not run when baseline persistence fails")

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            summary = run_pipeline(
                provider, snapshot, [_PartialFailureAction(), _MockAction("merge", ActionDecision.EXECUTE)]
            )

        assert summary.results[0].decision == ActionDecision.FAILED
        assert summary.results[1].decision == ActionDecision.SKIP
        assert "Failed to persist diff-preservation blocker" in caplog.text

    def test_failed_invalidating_action_reraises_rate_limit_during_blocker_persistence(self) -> None:
        """Rate limits while persisting a blocker must propagate."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "oldsha"
        provider.post_comment.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
        )
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", base_branch="main", files=["fix.py"])
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha", base_branch="main", files=[])

        class _PartialFailureAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="publish",
                    decision=ActionDecision.FAILED,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            with pytest.raises(ProviderRateLimitError):
                run_pipeline(provider, snapshot, [_PartialFailureAction()])

    def test_failed_invalidating_action_skips_blocker_persistence_when_live_head_missing(self) -> None:
        """A missing live HEAD no longer prevents blocker persistence."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = ""
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", base_branch="main", files=["fix.py"])
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha", base_branch="main", files=[])

        class _PartialFailureAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="publish",
                    decision=ActionDecision.FAILED,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            summary = run_pipeline(
                provider, snapshot, [_PartialFailureAction(), _MockAction("merge", ActionDecision.EXECUTE)]
            )

        assert summary.results[1].decision == ActionDecision.BLOCKED_BY_GUARD
        provider.post_comment.assert_not_called()

    def test_failed_invalidating_action_skips_blocker_persistence_for_stale_head(self) -> None:
        """A stale live HEAD no longer prevents persisting the trusted baseline."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "otherhead"
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", base_branch="main", files=["fix.py"])
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha", base_branch="main", files=[])

        class _PartialFailureAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="publish",
                    decision=ActionDecision.FAILED,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            summary = run_pipeline(
                provider, snapshot, [_PartialFailureAction(), _MockAction("merge", ActionDecision.EXECUTE)]
            )

        assert summary.results[1].decision == ActionDecision.BLOCKED_BY_GUARD
        provider.post_comment.assert_not_called()

    def test_failed_invalidating_action_logs_when_live_head_lookup_fails(self) -> None:
        """A live HEAD lookup failure prevents blocker persistence."""
        provider = MagicMock()
        provider.get_pr_metadata.side_effect = RuntimeError("metadata failed")
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", base_branch="main", files=["fix.py"])
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha", base_branch="main", files=[])

        class _PartialFailureAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="publish",
                    decision=ActionDecision.FAILED,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed_snapshot,
        ):
            summary = run_pipeline(
                provider, snapshot, [_PartialFailureAction(), _MockAction("merge", ActionDecision.EXECUTE)]
            )

        assert summary.results[1].decision == ActionDecision.BLOCKED_BY_GUARD
        provider.post_comment.assert_not_called()

    def test_failed_invalidating_action_reraises_rate_limit_during_live_head_lookup(self) -> None:
        """A rate limit during live HEAD lookup prevents blocker persistence."""
        provider = MagicMock()
        provider.get_pr_metadata.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
        )
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", base_branch="main", files=["fix.py"])

        class _PartialFailureAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="publish",
                    decision=ActionDecision.FAILED,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        with pytest.raises(ProviderRateLimitError):
            run_pipeline(provider, snapshot, [_PartialFailureAction()])

        provider.get_pr_metadata.assert_called_once_with(1)
        provider.post_comment.assert_not_called()

    def test_failed_invalidating_action_surfaces_refresh_failure_on_result(self) -> None:
        """A failed mutating action reports snapshot refresh failures on the same result."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", base_branch="main", files=["fix.py"])

        class _PartialFailureAction:
            @property
            def name(self):
                return "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="squash",
                    decision=ActionDecision.FAILED,
                    details="squash_post_repair failed",
                    error="squash failed",
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            side_effect=RuntimeError("refresh failed"),
        ) as mock_refresh:
            summary = run_pipeline(provider, snapshot, [_PartialFailureAction()])

        mock_refresh.assert_called_once_with(provider, 1, actionable_check_names=None)
        assert summary.results[0].decision == ActionDecision.FAILED
        assert "failed to refresh snapshot after potential partial mutation" in summary.results[0].details
        assert "refresh failed: refresh failed" in summary.results[0].error

    def test_second_invalidation_re_arms_the_snapshot_refresh(self) -> None:
        """A second invalidation refreshes again so no action sees a pre-invalidation snapshot."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", files=["fix.py"])
        first_refresh = PRStateSnapshot(pr_number=1, head_sha="sha_after_first", files=["fix.py"])
        second_refresh = PRStateSnapshot(pr_number=1, head_sha="sha_after_second", files=["fix.py"])
        observed: list[str] = []

        class _FirstInvalidatingAction:
            @property
            def name(self):
                return "apply_suggestions"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="apply_suggestions", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="apply_suggestions",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                )

        class _OptInInvalidatingAction:
            """Opt-in action that invalidates the snapshot a second time."""

            @property
            def name(self):
                return "dispatch_repair"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                observed.append(snapshot.head_sha)
                return ActionResult(name="dispatch_repair", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="dispatch_repair",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                )

        class _LaterOptInAction:
            @property
            def name(self):
                return "request_review"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                observed.append(snapshot.head_sha)
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            side_effect=[first_refresh, second_refresh],
        ) as mock_refresh:
            summary = run_pipeline(
                provider,
                snapshot,
                [_FirstInvalidatingAction(), _OptInInvalidatingAction(), _LaterOptInAction()],
            )

        assert mock_refresh.call_count == 2
        # The later opt-in action sees state gathered AFTER the second invalidation.
        assert observed == ["sha_after_first", "sha_after_first", "sha_after_second", "sha_after_second"]
        assert summary.snapshot is second_refresh
        assert [r.decision for r in summary.results] == [
            ActionDecision.EXECUTE,
            ActionDecision.EXECUTE,
            ActionDecision.EXECUTE,
        ]

    def test_second_invalidation_halts_later_non_opt_in_actions(self) -> None:
        """After a second invalidation, non-opt-in actions are halted naming the newest invalidator."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", files=["fix.py"])
        refreshed = PRStateSnapshot(pr_number=1, head_sha="newsha", files=["fix.py"])

        class _FirstInvalidatingAction:
            @property
            def name(self):
                return "apply_suggestions"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="apply_suggestions", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="apply_suggestions",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                )

        class _OptInInvalidatingAction:
            @property
            def name(self):
                return "dispatch_repair"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="dispatch_repair", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="dispatch_repair",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                )

        class _NonOptInAction:
            @property
            def name(self):
                return "merge"

            def evaluate(self, snapshot, derived) -> ActionResult:
                raise AssertionError("evaluate() should not run after the snapshot is invalidated")

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise AssertionError("execute() should not run after the snapshot is invalidated")

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            return_value=refreshed,
        ):
            summary = run_pipeline(
                provider,
                snapshot,
                [_FirstInvalidatingAction(), _OptInInvalidatingAction(), _NonOptInAction()],
            )

        assert summary.results[2].decision == ActionDecision.SKIP
        assert "dispatch_repair" in summary.results[2].details

    def test_second_invalidation_drops_squash_preserved_green(self) -> None:
        """The squash green-CI shortcut is not carried across a re-armed second refresh."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            ci_status="passing",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        first_refresh = PRStateSnapshot(
            pr_number=1,
            head_sha="squashedsha",
            ci_status="pending",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        second_refresh = PRStateSnapshot(
            pr_number=1,
            head_sha="repairedsha",
            ci_status="pending",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        observed_flags: list[bool] = []

        class _SquashAction:
            @property
            def name(self):
                return "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                derived.set("squash_preserved_green", True)
                derived.set("squash_preserved_green_sha", "squashedsha")
                return ActionResult(
                    name="squash",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                    preserves_diff_fingerprint=True,
                )

        class _OptInInvalidatingAction:
            @property
            def name(self):
                return "dispatch_repair"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                observed_flags.append(derived.get("squash_preserved_green", False))
                return ActionResult(name="dispatch_repair", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(
                    name="dispatch_repair",
                    decision=ActionDecision.EXECUTE,
                    invalidates_snapshot=True,
                )

        class _LaterOptInAction:
            @property
            def name(self):
                return "request_review"

            @property
            def runs_after_invalidation(self):
                return True

            def evaluate(self, snapshot, derived) -> ActionResult:
                observed_flags.append(derived.get("squash_preserved_green", False))
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="request_review", decision=ActionDecision.EXECUTE)

        with patch(
            "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
            side_effect=[first_refresh, second_refresh],
        ):
            run_pipeline(
                provider,
                snapshot,
                [_SquashAction(), _OptInInvalidatingAction(), _LaterOptInAction()],
            )

        # Carried across the first refresh (SHA matches), dropped after the second
        # invalidation moved HEAD off the recorded post-squash SHA.
        assert observed_flags == [True, True, False, False]

    def test_skip_actions_not_blocked_after_failure(self) -> None:
        """All actions after a failure are halted (exec_failed_by gate is before evaluate)."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)

        class _FailingAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.FAILED)

        actions: list[Action] = [
            _FailingAction(),
            _MockAction("request_review", ActionDecision.SKIP),
        ]
        summary = run_pipeline(provider, snapshot, actions)
        assert summary.results[0].decision == ActionDecision.FAILED
        # Subsequent action is halted by exec_failed_by gate (before evaluate)
        assert summary.results[1].decision == ActionDecision.SKIP
        assert "halted" in summary.results[1].details.lower()

    def test_recovery_action_runs_after_prior_failure(self) -> None:
        """Recovery actions evaluate and execute while ordinary actions remain halted."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)
        assert DispatchRepairAction.runs_on_prior_failure is True

        class _TrackingAction(_MockAction):
            def __init__(self, name, eval_decision, exec_decision, *, runs_on_prior_failure=False):
                super().__init__(name, eval_decision, exec_decision)
                self.runs_on_prior_failure = runs_on_prior_failure
                self.evaluate_calls = 0
                self.execute_calls = 0

            def evaluate(self, snapshot, derived):
                self.evaluate_calls += 1
                return super().evaluate(snapshot, derived)

            def execute(self, provider, snapshot, derived):
                self.execute_calls += 1
                return super().execute(provider, snapshot, derived)

        failing = _TrackingAction("takeover", ActionDecision.EXECUTE, ActionDecision.FAILED)
        recovery = _TrackingAction(
            "dispatch_repair",
            ActionDecision.EXECUTE,
            ActionDecision.EXECUTE,
            runs_on_prior_failure=True,
        )
        halted = _TrackingAction("request_review", ActionDecision.EXECUTE, ActionDecision.EXECUTE)

        summary = run_pipeline(provider, snapshot, [failing, recovery, halted])

        assert summary.results[0].decision == ActionDecision.FAILED
        assert summary.results[1].decision == ActionDecision.EXECUTE
        assert recovery.evaluate_calls == 2
        assert recovery.execute_calls == 1
        assert summary.results[2].decision == ActionDecision.SKIP
        assert halted.evaluate_calls == 0
        assert halted.execute_calls == 0

    def test_summary_has_run_url_and_timestamp(self, monkeypatch) -> None:
        """Summary includes run_url and timestamp."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)
        actions: list[Action] = []

        # Set env vars for run URL
        monkeypatch.setenv("GITHUB_SERVER_URL", "https://github.com")
        monkeypatch.setenv("GITHUB_REPOSITORY", "org/repo")
        monkeypatch.setenv("GITHUB_RUN_ID", "12345")

        summary = run_pipeline(provider, snapshot, actions)
        assert summary.run_url == "https://github.com/org/repo/actions/runs/12345"
        assert summary.timestamp != ""

    def test_no_log_group_annotations_outside_github_actions(self, monkeypatch, capsys) -> None:
        """No ::group:: annotations should be emitted outside GitHub Actions."""
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)

        summary = run_pipeline(
            MagicMock(),
            PRStateSnapshot(pr_number=1),
            [_MockAction("publish", ActionDecision.EXECUTE)],
        )
        captured = capsys.readouterr()
        assert summary.results[0].decision == ActionDecision.EXECUTE
        assert "::group::" not in captured.err
        assert "::endgroup::" not in captured.err

    def test_summary_has_empty_run_url_without_actions_env(self, monkeypatch) -> None:
        """Run URL is empty when GitHub Actions environment is incomplete."""
        monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
        monkeypatch.delenv("GITHUB_RUN_ID", raising=False)
        monkeypatch.delenv("TRIGGER_REASON", raising=False)
        summary = run_pipeline(MagicMock(), PRStateSnapshot(pr_number=1), [])
        assert summary.run_url == ""

    def test_log_helpers_noop_outside_github_actions(self, monkeypatch) -> None:
        """When not in GitHub Actions, _log_group/_log_endgroup are no-ops."""
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)
        actions = [_MockAction("approve", ActionDecision.EXECUTE)]
        summary = run_pipeline(provider, snapshot, actions)
        assert summary.results[0].decision == ActionDecision.EXECUTE

    def test_log_helpers_emit_annotations_in_github_actions(self, monkeypatch, capsys) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")

        _log_group("checks")
        _log_endgroup()

        assert capsys.readouterr().err == "::group::checks\n::endgroup::\n"

    def test_non_guards_blocked_does_not_set_guard_block(self) -> None:
        """A non-guards action returning BLOCKED does not set guard_blocked."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)

        class _BlockingAction:
            @property
            def name(self):
                return "publish"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.BLOCKED, details="blocked")

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="publish", decision=ActionDecision.EXECUTE)

        summary = run_pipeline(provider, snapshot, [_BlockingAction(), _MockAction("approve", ActionDecision.EXECUTE)])
        assert summary.results[0].decision == ActionDecision.BLOCKED
        # Subsequent actions are NOT blocked by guard
        assert summary.results[1].decision == ActionDecision.EXECUTE

    def test_guards_execute_exception_does_not_halt_pipeline(self) -> None:
        """Guards execute() exception → FAILED but exec_failed_by not set."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1)

        class _ExplodingGuards:
            @property
            def name(self):
                return "guards"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="guards", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                raise RuntimeError("guards exploded")

        summary = run_pipeline(provider, snapshot, [_ExplodingGuards(), _MockAction("publish", ActionDecision.EXECUTE)])
        assert summary.results[0].decision == ActionDecision.FAILED
        assert "guards exploded" in summary.results[0].error
        # exec_failed_by is not set for guards, so publish still runs
        assert summary.results[1].decision == ActionDecision.EXECUTE

    def test_summary_includes_trigger_reason_from_env(self, monkeypatch) -> None:
        """Summary captures TRIGGER_REASON from environment."""
        monkeypatch.setenv("TRIGGER_REASON", "agent_session_finished")
        summary = run_pipeline(MagicMock(), PRStateSnapshot(pr_number=1), [])
        assert summary.trigger_reason == "agent_session_finished"

    def test_summary_has_empty_trigger_reason_when_env_not_set(self, monkeypatch) -> None:
        """trigger_reason is empty when TRIGGER_REASON env var is not set."""
        monkeypatch.delenv("TRIGGER_REASON", raising=False)
        summary = run_pipeline(MagicMock(), PRStateSnapshot(pr_number=1), [])
        assert summary.trigger_reason == ""

    def test_all_8_actions_evaluated_on_ci_completion(self) -> None:
        """All 8 actions evaluated on a CI completion event."""
        provider = MagicMock()
        snapshot = self._make_pipeline_snapshot()
        actions = self._make_pipeline_actions()
        summary = run_pipeline(provider, snapshot, actions)
        assert len(summary.results) == 8
        action_names = [r.name for r in summary.results]
        assert action_names == [
            "guards",
            "publish",
            "dispatch_repair",
            "resolve_threads",
            "squash",
            "request_review",
            "approve",
            "merge",
        ]

    def test_pipeline_actions_fixture_matches_production_order(self) -> None:
        """The runner fixture is a subsequence of the production pipeline order.

        ``_make_pipeline_actions`` deliberately exercises a subset of the twelve
        production actions, but its relative order must match the one built by
        ``run_ai_pr_loop_v2`` — otherwise the fixture can assert an ordering the
        pipeline never runs (e.g. request_review before resolve_threads, under
        which post-resolution invalidation is impossible).
        """
        from agentic_devtools.cli.ci.models import EventPayload
        from agentic_devtools.cli.ci.pipeline.command import run_ai_pr_loop_v2

        with (
            patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", return_value="token"),
            patch("agentic_devtools.cli.ci.pipeline.command.release_lock"),
            patch(
                "agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot",
                return_value=MagicMock(),
            ),
            patch("agentic_devtools.cli.ci.pipeline.command.run_pipeline") as mock_run_pipeline,
            patch("agentic_devtools.cli.ci.pipeline.command.post_summary_comment"),
            patch("agentic_devtools.cli.ci.pipeline.command._determine_exit_code", return_value=0),
        ):
            run_ai_pr_loop_v2(MagicMock(), EventPayload(pr_number=1))

        production_names = [action.name for action in mock_run_pipeline.call_args.args[2]]
        fixture_names = [action.name for action in self._make_pipeline_actions()]

        assert set(fixture_names) <= set(production_names)
        assert fixture_names == [name for name in production_names if name in set(fixture_names)]

    def test_all_8_actions_evaluated_on_review_submission(self) -> None:
        """All 8 actions evaluated on a review submission event."""
        provider = MagicMock()
        snapshot = self._make_pipeline_snapshot()
        actions = self._make_pipeline_actions()
        summary = run_pipeline(provider, snapshot, actions)
        assert len(summary.results) == 8

    def test_all_8_actions_evaluated_on_issue_comment(self) -> None:
        """All 8 actions evaluated on an issue_comment event."""
        provider = MagicMock()
        snapshot = self._make_pipeline_snapshot()
        actions = self._make_pipeline_actions()
        summary = run_pipeline(provider, snapshot, actions)
        assert len(summary.results) == 8

    def test_three_trigger_types_produce_identical_evaluations(self) -> None:
        """Different trigger types with same state produce identical evaluations."""
        snapshot = self._make_pipeline_snapshot()
        actions = self._make_pipeline_actions()
        results_per_trigger = []

        for _ in range(3):
            provider = MagicMock()
            summary = run_pipeline(provider, snapshot, actions)
            results_per_trigger.append([(r.name, r.decision) for r in summary.results])

        assert results_per_trigger[0] == results_per_trigger[1]
        assert results_per_trigger[1] == results_per_trigger[2]

    def test_two_runs_same_state_same_decisions(self) -> None:
        """Running pipeline twice on unchanged state produces identical decisions."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="abc123",
            base_branch="main",
            head_branch="feature",
            commit_count=1,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            active_session=False,
            copilot_review_pending=False,
            unresolved_threads=0,
            labels=["ai-auto-merge-allowed"],
            is_draft=False,
            mergeable=True,
            has_approval_on_head=True,
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            files=["src/main.py"],
            has_changes=True,
        )

        # Intentionally omit DispatchRepairAction: this deterministic scenario
        # asserts decision stability without exercising dedup/cycle-limit probes.
        actions: list[Action] = [
            GuardsAction(),
            PublishAction(),
            RequestReviewAction(),
            ResolveThreadsAction(),
            SquashAction(),
            ApproveAction(),
            MergeAction(),
        ]

        provider1 = MagicMock()
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.request_review.is_copilot_session_active_via_agent_task",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.approve.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.merge.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
        ):
            provider1 = MagicMock()
            provider1.get_pr_metadata.return_value.head_sha = snapshot.head_sha
            summary1 = run_pipeline(provider1, snapshot, actions)

            provider2 = MagicMock()
            provider2.get_pr_metadata.return_value.head_sha = snapshot.head_sha
            summary2 = run_pipeline(provider2, snapshot, actions)

        assert len(summary1.results) == len(summary2.results)
        for r1, r2 in zip(summary1.results, summary2.results):
            assert r1.decision == r2.decision, f"Action '{r1.name}' decisions differ"

        assert summary1.results[0].decision == ActionDecision.EXECUTE
        assert summary1.results[1].decision == ActionDecision.SKIP
        assert summary1.results[2].decision == ActionDecision.SKIP
        assert summary1.results[3].decision == ActionDecision.SKIP
        assert summary1.results[4].decision == ActionDecision.SKIP
        assert summary1.results[5].decision == ActionDecision.EXECUTE
        assert summary1.results[6].decision == ActionDecision.EXECUTE

        provider1.merge_pr.assert_called_once()
        provider2.merge_pr.assert_called_once()

    def test_merge_stays_blocked_when_approval_submit_skips_and_only_loop_signal_was_true(self) -> None:
        """A skipped approval must not let merge reuse a stale non-precise approval signal."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="abc123",
            base_branch="main",
            head_branch="feature",
            commit_count=1,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            active_session=False,
            copilot_review_pending=False,
            unresolved_threads=0,
            labels=["ai-auto-merge-allowed"],
            is_draft=False,
            mergeable=True,
            has_approval_on_head=True,
            has_approver_approval_on_head=False,
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            files=["src/main.py"],
            has_changes=True,
        )
        actions: list[Action] = [
            GuardsAction(),
            ApproveAction(),
            MergeAction(),
        ]
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = snapshot.head_sha
        provider.approve_pr.return_value = False

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.approve.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.merge.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
        ):
            summary = run_pipeline(provider, snapshot, actions)

        assert [result.decision for result in summary.results] == [
            ActionDecision.EXECUTE,
            ActionDecision.SKIP,
            ActionDecision.SKIP,
        ]
        assert summary.results[1].preconditions == {"approver_token_available": False}
        assert summary.results[2].preconditions.get("approved") is False
        provider.approve_pr.assert_called_once()
        provider.merge_pr.assert_not_called()

    def test_fifty_runs_no_state_change(self) -> None:
        """50 runs on an already-complete state produce 0 non-guard executions."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="abc123",
            base_branch="main",
            head_branch="feature",
            commit_count=1,
            ci_status="pending",
            review_state="",
            copilot_review_id=0,
            active_session=False,
            copilot_review_pending=True,
            unresolved_threads=0,
            labels=[],
            is_draft=False,
            mergeable=True,
            has_approval_on_head=False,
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            files=["src/main.py"],
            has_changes=True,
        )

        # Intentionally omit DispatchRepairAction to keep this loop focused on
        # no-op waiting behavior without provider dedup/cycle-limit checks.
        actions: list[Action] = [
            GuardsAction(),
            PublishAction(),
            RequestReviewAction(),
            ResolveThreadsAction(),
            SquashAction(),
            ApproveAction(),
            MergeAction(),
        ]

        for _ in range(50):
            provider = MagicMock()
            summary = run_pipeline(provider, snapshot, actions)
            executed = [r for r in summary.results if r.decision == ActionDecision.EXECUTE]
            assert len(executed) == 1
            assert executed[0].name == "guards"
            provider.merge_pr.assert_not_called()
            provider.approve_pr.assert_not_called()
            provider.publish_pr.assert_not_called()
            provider.dispatch_repair.assert_not_called()

    def test_review_request_can_run_after_dispatch_repair_review_dedup_skip(self) -> None:
        """Review request can still run when dispatch repair dedup path skips."""
        provider = verified_pr_provider(1, "oldsha", ["fix.py"], post_squash_head_sha="newsha")
        # Exhausted opaque review work now lives in the durable HEAD ledger.
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.find_comment.return_value = None
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=7,
                author="trusted-bot",
                body='<!-- repair-dispatch-findings:1:oldsha:v1 -->\n{"attempted": ["review:4401589029"]}',
            )
        ]
        provider.list_review_comments.return_value = []
        provider.list_review_thread_states.return_value = {}
        provider.post_comment.return_value = 1
        # Build a suppressed-only block that is still actionable for dispatch_repair
        # while the shared review gate passes via a matching repair-satisfied marker.
        initial_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            base_branch="main",
            head_branch="feature",
            commit_count=2,
            ci_status="passing",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
            review_state="APPROVED",
            copilot_review_id=0,
            copilot_review_inline_count=0,
            unresolved_threads=0,
            repair_satisfied_review_id=4401589029,
            repairable_threads=1,
            reviews=[
                ReviewInfo(id=4401589029, user="Copilot", state="COMMENTED"),
            ],
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_SUPPRESSED_COMMENTS,
                review_id=4401589029,
                body_comment_count=0,
                suppressed_count=2,
            ),
            is_draft=False,
            copilot_review_pending=False,
            base_repo_full_name="org/repo",
        )
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="newsha",
            base_branch="main",
            head_branch="feature",
            commit_count=1,
            ci_status="passing",
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
            review_state="",
            copilot_review_id=0,
            copilot_review_inline_count=0,
            unresolved_threads=0,
            is_draft=False,
            copilot_review_pending=False,
            base_repo_full_name="org/repo",
        )
        actions: list[Action] = [
            DispatchRepairAction(),
            SquashAction(),
            RequestReviewAction(),
        ]

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=True,
            ) as duplicate_trigger,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.squash.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.request_review.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.runner.build_pr_state_snapshot",
                return_value=refreshed_snapshot,
            ),
        ):
            summary = run_pipeline(provider, initial_snapshot, actions)

        assert [r.decision for r in summary.results] == [
            ActionDecision.SKIP,
            ActionDecision.EXECUTE,
            ActionDecision.EXECUTE,
        ]
        duplicate_trigger.assert_not_called()
        provider.add_label.assert_called_once_with(1, "ai-pr-loop:agent-failed")
        assert summary.results[2].preconditions.get("no_repair_dispatched") is True
        provider.dispatch_repair.assert_not_called()
        provider.squash_post_repair.assert_called_once()
        provider.request_reviewer.assert_called_once()

    @pytest.mark.parametrize("review_state", ["COMMENTED", "CHANGES_REQUESTED", "APPROVED"])
    def test_review_request_stops_after_repair_dedup_limit_when_gate_is_blocked(self, review_state: str) -> None:
        """Unresolved body-only work escalates instead of requesting another review."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head-sha",
            ci_status="passing",
            review_state=review_state,
            copilot_review_id=100,
            copilot_review_inline_count=1 if review_state == "COMMENTED" else 0,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_HAS_COMMENTS,
                review_id=100,
            ),
            is_draft=False,
            copilot_review_pending=False,
            unresolved_threads=0,
            base_repo_full_name="org/repo",
        )
        provider = MagicMock()
        provider.find_comment.return_value = None
        provider.list_review_comments.return_value = []
        provider.list_review_thread_states.return_value = {}
        provider.post_comment.return_value = 1
        actions: list[Action] = [DispatchRepairAction(), RequestReviewAction()]

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(True, 8),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.reconcile",
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.request_review.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
        ):
            summary = run_pipeline(provider, snapshot, actions)

        assert [result.decision for result in summary.results] == [
            ActionDecision.SKIP,
            ActionDecision.SKIP,
        ]
        assert summary.results[0].limit_reached is True
        assert summary.results[0].escalation_needed is True
        provider.add_label.assert_called_once_with(1, "ai-pr-loop:agent-failed")
        provider.post_comment.assert_called_once()
        provider.request_reviewer.assert_not_called()

    def test_dedup_limit_with_ci_only_work_does_not_escalate(self) -> None:
        """A CI-only repair reaching the global limit does not trigger review escalation."""
        snapshot = PRStateSnapshot(pr_number=42, head_sha="head-sha", ci_status="failing")
        provider = MagicMock()
        provider.find_comment.return_value = None
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = []

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(True, 8),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
        ):
            summary = run_pipeline(provider, snapshot, [DispatchRepairAction()])

        assert summary.results[0].decision == ActionDecision.SKIP
        assert summary.results[0].dedup_limit_reached is True
        assert summary.results[0].escalation_needed is False
        provider.add_label.assert_not_called()
        provider.post_comment.assert_not_called()

    def test_review_request_stops_after_repair_cycle_limit_when_gate_is_blocked(self) -> None:
        """A global repair cycle limit must stop for human intervention."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head-sha",
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_HAS_COMMENTS,
                review_id=100,
            ),
            is_draft=False,
            copilot_review_pending=False,
            unresolved_threads=0,
            base_repo_full_name="org/repo",
        )
        provider = MagicMock()
        provider.find_comment.return_value = None
        provider.list_review_comments.return_value = []
        provider.list_review_thread_states.return_value = {}
        actions: list[Action] = [DispatchRepairAction(), RequestReviewAction()]

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(True, 50),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.request_review.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
        ):
            summary = run_pipeline(provider, snapshot, actions)

        assert [result.decision for result in summary.results] == [
            ActionDecision.SKIP,
            ActionDecision.SKIP,
        ]
        assert summary.results[0].limit_reached is True
        assert summary.results[0].cycle_limit_reached is True
        assert "human intervention" in summary.results[1].details.lower()
        provider.request_reviewer.assert_not_called()

    @pytest.mark.parametrize("comment_fails", [False, True])
    def test_dedup_exhaustion_escalates_and_skips_review_request(self, comment_fails: bool) -> None:
        root = ReviewCommentInfo(id=101, path="a.py", body="Fix this", html_url="https://example/101")
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="head-sha",
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            repairable_threads=1,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot-pull-request-reviewer[bot]",
                    state="CHANGES_REQUESTED",
                    commit_sha="head-sha",
                )
            ],
            is_draft=False,
        )
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = []
        provider.list_review_comments.return_value = [root]
        provider.list_review_thread_states.return_value = {}
        provider.find_comment.return_value = None
        provider.post_comment.return_value = 1
        if comment_fails:
            provider.post_comment.side_effect = RuntimeError("comment write failed")
        actions: list[Action] = [DispatchRepairAction(), RequestReviewAction()]

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(True, 8),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
        ):
            summary = run_pipeline(provider, snapshot, actions)

        if comment_fails:
            assert summary.results[0].decision == ActionDecision.FAILED
            assert "dispatch_repair" in summary.results[1].details
        else:
            assert [result.decision for result in summary.results] == [
                ActionDecision.SKIP,
                ActionDecision.SKIP,
            ]
            assert summary.results[0].escalation_needed is True
            assert summary.results[1].preconditions["no_repair_escalation_needed"] is False
        provider.add_label.assert_called_once_with(42, "ai-pr-loop:agent-failed")
        provider.request_reviewer.assert_not_called()

    def test_coding_agent_review_does_not_suppress_current_head_ccr_request(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="head-sha",
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=200,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot-pull-request-reviewer[bot]",
                    state="CHANGES_REQUESTED",
                    commit_sha="stale-sha",
                ),
                ReviewInfo(
                    id=200,
                    user="copilot-swe-agent[bot]",
                    state="COMMENTED",
                    commit_sha="head-sha",
                ),
            ],
            is_draft=False,
        )
        provider = verified_pr_provider(42, "head-sha", ["src/main.py"])

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.request_review.is_copilot_session_active_via_agent_task",
            return_value=False,
        ):
            summary = run_pipeline(provider, snapshot, [RequestReviewAction()])

        assert summary.results[0].decision == ActionDecision.EXECUTE
        assert summary.results[0].preconditions["no_effective_review_on_head"] is True
        provider.request_reviewer.assert_called_once()

    def _make_pipeline_snapshot(self) -> PRStateSnapshot:
        return PRStateSnapshot(
            pr_number=1,
            head_sha="abc123",
            base_branch="main",
            head_branch="feature",
            commit_count=1,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            active_session=False,
            copilot_review_pending=False,
            unresolved_threads=0,
            labels=[],
            is_draft=False,
            mergeable=True,
            has_approval_on_head=True,
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            files=["src/main.py"],
            has_changes=True,
        )

    def _make_pipeline_actions(self) -> list[Action]:
        """Return a subset of the production pipeline, in production order.

        The order is asserted against the real builder in
        ``test_pipeline_actions_fixture_matches_production_order`` so this fixture
        can never silently diverge from ``run_ai_pr_loop_v2``.
        """
        return [
            GuardsAction(),
            PublishAction(),
            DispatchRepairAction(),
            ResolveThreadsAction(),
            SquashAction(),
            RequestReviewAction(),
            ApproveAction(),
            MergeAction(),
        ]
