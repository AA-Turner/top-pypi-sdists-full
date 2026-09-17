"""Tests for run_pipeline."""

import base64
import hashlib
import json
import logging
import os
import zlib
from datetime import UTC, datetime
from unittest.mock import MagicMock, call, patch

import pytest

from agentic_devtools.cli.ci.models import IssueCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions import (
    ApproveAction,
    DispatchRepairAction,
    GuardsAction,
    MergeAction,
    PublishAction,
    RequestReviewAction,
    ResolveThreadsAction,
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
from agentic_devtools.cli.ci.pipeline.snapshot import PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class _MockAction:
    """A mock action for testing the runner."""

    def __init__(
        self,
        name: str,
        eval_decision: ActionDecision,
        exec_decision: ActionDecision | None = None,
        definitive_no_mutation: bool = False,
        may_invalidate_snapshot: bool = False,
    ):
        self._name = name
        self._eval_decision = eval_decision
        self._exec_decision = exec_decision
        self._definitive_no_mutation = definitive_no_mutation
        self.may_invalidate_snapshot = may_invalidate_snapshot

    @property
    def name(self) -> str:
        return self._name

    def evaluate(self, snapshot, derived) -> ActionResult:
        return ActionResult(name=self._name, decision=self._eval_decision, details=f"eval_{self._name}")

    def execute(self, provider, snapshot, derived) -> ActionResult:
        decision = self._exec_decision or ActionDecision.EXECUTE
        return ActionResult(
            name=self._name,
            decision=decision,
            details=f"exec_{self._name}",
            definitive_no_mutation=self._definitive_no_mutation,
        )


def _diff_preservation_blocker_comment(payload: dict[str, object]) -> str:
    payload = {"allowed_removed_files": [], **payload}
    encoded = base64.urlsafe_b64encode(
        zlib.compress(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode(), level=9)
    ).decode()
    return f"<!-- agdt:diff-preservation-blocker:{encoded.rstrip('=')} -->"


class TestRunPipeline:
    """Tests for the pipeline runner."""

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
        provider.post_comment_as_pr_token.assert_called_once()
        persisted_marker = provider.post_comment_as_pr_token.call_args.args[1]
        encoded_payload = persisted_marker.removeprefix("<!-- agdt:diff-preservation-blocker:").removesuffix(" -->")
        persisted_payload = json.loads(zlib.decompress(base64.urlsafe_b64decode(encoded_payload + "==")))
        assert persisted_payload["baseline_head"] == "oldsha"
        assert persisted_payload["baseline_files"] == ["fix.py"]
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
        assert provider.post_comment_as_pr_token.call_count == 2
        persisted_marker = provider.post_comment_as_pr_token.call_args.args[1]
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

        provider.post_comment_as_pr_token.assert_not_called()

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

        assert seen_heads == ["newsha"]
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
        assert provider.post_comment_as_pr_token.call_args_list[-1] == call(
            1,
            _diff_preservation_blocker_comment(
                {
                    "baseline_head": "oldsha",
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
        provider.post_comment_as_pr_token.assert_called_once_with(
            1,
            "<!-- agdt:diff-preservation-blocker-cleared:feedbeef -->",
        )

    @patch.dict(os.environ, {"GITHUB_ACTOR": "github-actions[bot]"}, clear=False)
    def test_persist_diff_preservation_blocker_updates_active_summary_comment(self) -> None:
        """When an active summary comment exists, the blocker is embedded in it."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "oldsha"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=500,
                author="github-actions[bot]",
                body="<!-- agdt:ai-pr-loop-summary -->\n#### 🤖 AI PR Loop Run\nDetails",
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
        provider.post_comment_as_pr_token.assert_not_called()

    @patch.dict(os.environ, {"GITHUB_ACTOR": "github-actions[bot]"}, clear=False)
    def test_persist_diff_preservation_blocker_replaces_existing_marker_in_summary(self) -> None:
        """When an existing blocker marker is already present in summary, it is replaced."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "oldsha"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=500,
                author="github-actions[bot]",
                body=(
                    "<!-- agdt:ai-pr-loop-summary -->\n"
                    "#### 🤖 AI PR Loop Run\n"
                    "<!-- agdt:diff-preservation-blocker:bm90LWpzb24 -->"
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
    def test_clear_diff_preservation_blocker_strips_summary_and_deletes_standalone(self) -> None:
        """Clearing removes the blocker from summary and deletes legacy standalone comments."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
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
        assert provider.post_comment_as_pr_token.call_args_list[1].args == (
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
        provider.post_comment_as_pr_token.assert_not_called()

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
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP
        provider.compute_diff_hash.assert_called_once_with(base_branch="main", sha="prehead")
        provider.post_comment_as_pr_token.assert_called_once_with(
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
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.BLOCKED_BY_GUARD
        assert "fingerprint unavailable" in summary.results[0].details

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
        provider.post_comment_as_pr_token.side_effect = RuntimeError("comment failed")
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
        provider.post_comment_as_pr_token.side_effect = ProviderRateLimitError(
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
        provider.post_comment_as_pr_token.assert_not_called()
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
        provider.post_comment_as_pr_token.assert_not_called()
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
        provider.post_comment_as_pr_token.assert_not_called()
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
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )

        summary = run_pipeline(provider, snapshot, [_MockAction("guards", ActionDecision.SKIP)])

        assert summary.results[0].decision == ActionDecision.SKIP
        provider.post_comment_as_pr_token.assert_called_once_with(
            1,
            "<!-- agdt:conflict-repair-validated:feedbeef -->",
        )

    def test_newer_validated_marker_for_different_head_consumes_dispatch(self) -> None:
        """A newer validation marker consumes the older dispatch by comment ordering."""
        provider = MagicMock()
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
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
        marker_time = datetime.now(UTC).isoformat()
        provider.find_comment.side_effect = [
            None,
            (1, f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->"),
            None,
        ]
        provider.compute_diff_hash.return_value = "same-hash"
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        provider.post_comment_as_pr_token.side_effect = RuntimeError("comment failed")
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
        provider.post_comment_as_pr_token.side_effect = ProviderRateLimitError(
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

    def test_recent_conflict_repair_marker_with_unavailable_pre_hash_blocks_pipeline(self) -> None:
        """A capable provider returning None for the baseline fingerprint fails closed."""
        provider = MagicMock()
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

    def test_recent_conflict_repair_marker_with_empty_pre_hash_blocks_pipeline(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """An empty baseline fingerprint string is treated as unavailable and logged."""
        provider = MagicMock()
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
            files=["fix.py"],
            diff_hash="same-hash",
            diff_hash_supported=True,
            diff_hash_available=True,
        )
        refreshed_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="finalhead",
            base_branch="main",
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
        assert provider.post_comment_as_pr_token.call_args_list == [
            call(
                1,
                _diff_preservation_blocker_comment(
                    {
                        "baseline_head": "feedbeef",
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
        provider.post_comment_as_pr_token.assert_called_once_with(
            1,
            _diff_preservation_blocker_comment(
                {
                    "baseline_head": "feedbeef",
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
        provider.post_comment_as_pr_token.assert_called_once()
        encoded_payload = (
            provider.post_comment_as_pr_token.call_args.args[1]
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
        provider.post_comment_as_pr_token.assert_called_once()
        encoded_payload = (
            provider.post_comment_as_pr_token.call_args.args[1]
            .removeprefix("<!-- agdt:diff-preservation-blocker:")
            .removesuffix(" -->")
        )
        persisted_payload = json.loads(zlib.decompress(base64.urlsafe_b64decode(encoded_payload + "==")))
        assert persisted_payload == {
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
        assert provider.post_comment_as_pr_token.call_args_list == [
            call(1, "<!-- agdt:conflict-repair-validated:newhead -->"),
            call(1, "<!-- agdt:diff-preservation-blocker-cleared:newhead -->"),
        ]

    def test_failed_conflict_repair_validation_persistence_keeps_blocker(self) -> None:
        """A failed validation marker post keeps the cross-run blocker armed."""
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.get_pr_metadata.return_value.head_sha = "newhead"
        provider.post_comment_as_pr_token.side_effect = RuntimeError("post failed")
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
        provider.post_comment_as_pr_token.assert_called_once_with(
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
        assert observed == ["newsha", "newsha"]
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

        assert observed == [True]

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

        assert observed == [False]

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
        assert observed == [0]
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
        persisted_marker = provider.post_comment_as_pr_token.call_args.args[1]
        assert persisted_marker.startswith("<!-- agdt:diff-preservation-blocker:")

    def test_failed_invalidating_action_refreshes_immediately_and_blocks_dropped_diff(self) -> None:
        """A failed mutating action still refreshes and validates the pushed HEAD."""
        provider = MagicMock()
        provider.get_pr_metadata.side_effect = [
            MagicMock(head_sha="oldsha"),
            MagicMock(head_sha="newsha"),
        ]
        provider.post_comment_as_pr_token.side_effect = [RuntimeError("comment failed"), None]
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
        assert provider.post_comment_as_pr_token.call_count == 1
        persisted_marker = provider.post_comment_as_pr_token.call_args.args[1]
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
        assert provider.post_comment_as_pr_token.call_count == 2
        marker = provider.post_comment_as_pr_token.call_args.args[1]
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
        provider.post_comment_as_pr_token.side_effect = RuntimeError("comment failed")
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
        provider.post_comment_as_pr_token.side_effect = ProviderRateLimitError(
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
        provider.post_comment_as_pr_token.assert_not_called()

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
        provider.post_comment_as_pr_token.assert_not_called()

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
        provider.post_comment_as_pr_token.assert_not_called()

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
        provider.post_comment_as_pr_token.assert_not_called()

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
        assert observed == ["sha_after_first", "sha_after_second"]
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
        assert observed_flags == [True, False]

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
        assert recovery.evaluate_calls == 1
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
                "agentic_devtools.cli.ci.pipeline.actions.approve.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.merge.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
        ):
            provider1 = MagicMock()
            summary1 = run_pipeline(provider1, snapshot, actions)

            provider2 = MagicMock()
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
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "oldsha"
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
        duplicate_trigger.assert_called_once_with(provider, 1, 4401589029)
        assert summary.results[2].preconditions.get("no_repair_dispatched") is True
        provider.dispatch_repair.assert_not_called()
        provider.squash_post_repair.assert_called_once()
        provider.request_reviewer.assert_called_once()

    @pytest.mark.parametrize("review_state", ["COMMENTED", "CHANGES_REQUESTED", "APPROVED"])
    def test_review_request_runs_after_repair_dedup_limit_when_gate_is_blocked(self, review_state: str) -> None:
        """A repair dedup limit must not suppress a fresh review for a blocked gate."""
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
            ActionDecision.EXECUTE,
        ]
        assert summary.results[0].limit_reached is True
        provider.request_reviewer.assert_called_once()

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
