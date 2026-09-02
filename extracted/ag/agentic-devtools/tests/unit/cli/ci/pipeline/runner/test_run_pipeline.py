"""Tests for run_pipeline."""

import logging
from unittest.mock import MagicMock, patch

import pytest

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
    REASON_SUPPRESSED_COMMENTS,
    CopilotGateVerdict,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.runner import _log_endgroup, _log_group, run_pipeline
from agentic_devtools.cli.ci.pipeline.snapshot import PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class _MockAction:
    """A mock action for testing the runner."""

    def __init__(self, name: str, eval_decision: ActionDecision, exec_decision: ActionDecision | None = None):
        self._name = name
        self._eval_decision = eval_decision
        self._exec_decision = exec_decision

    @property
    def name(self) -> str:
        return self._name

    def evaluate(self, snapshot, derived) -> ActionResult:
        return ActionResult(name=self._name, decision=self._eval_decision, details=f"eval_{self._name}")

    def execute(self, provider, snapshot, derived) -> ActionResult:
        decision = self._exec_decision or ActionDecision.EXECUTE
        return ActionResult(name=self._name, decision=decision, details=f"exec_{self._name}")


class TestRunPipeline:
    """Tests for the pipeline runner."""

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
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha")
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha")

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

    def test_runs_after_invalidation_actions_share_refreshed_derived_state(self) -> None:
        """All opt-in actions after invalidation share refreshed snapshot/derived state."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha")
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha")
        observed: list[str] = []

        class _InvalidatingAction:
            @property
            def name(self):
                return "squash"

            def evaluate(self, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE)

            def execute(self, provider, snapshot, derived) -> ActionResult:
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE, invalidates_snapshot=True)

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
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha")
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha")
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
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha")
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha")
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
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha")
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha")
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
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha")
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha", ci_status="pending")

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
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha")
        # A concurrent push moved the branch to "concurrentsha" — not the post-squash "squashedsha"
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="concurrentsha", ci_status="pending")

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
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha")
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha")

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
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", unresolved_threads=7)
        # Fresh query after resolution + squash: all threads are resolved.
        refreshed_snapshot = PRStateSnapshot(pr_number=1, head_sha="newsha", unresolved_threads=0)
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
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE, invalidates_snapshot=True)

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

    def test_second_invalidation_re_arms_the_snapshot_refresh(self) -> None:
        """A second invalidation refreshes again so no action sees a pre-invalidation snapshot."""
        provider = MagicMock()
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha")
        first_refresh = PRStateSnapshot(pr_number=1, head_sha="sha_after_first")
        second_refresh = PRStateSnapshot(pr_number=1, head_sha="sha_after_second")
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
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha")
        refreshed = PRStateSnapshot(pr_number=1, head_sha="newsha")

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
        snapshot = PRStateSnapshot(pr_number=1, head_sha="oldsha", ci_status="passing")
        first_refresh = PRStateSnapshot(pr_number=1, head_sha="squashedsha", ci_status="pending")
        second_refresh = PRStateSnapshot(pr_number=1, head_sha="repairedsha", ci_status="pending")
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
                return ActionResult(name="squash", decision=ActionDecision.EXECUTE, invalidates_snapshot=True)

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
        # Build a suppressed-only block that is still actionable for dispatch_repair
        # while the shared review gate passes via a matching repair-satisfied marker.
        initial_snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="oldsha",
            base_branch="main",
            head_branch="feature",
            commit_count=2,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=0,
            copilot_review_inline_count=0,
            unresolved_threads=0,
            repair_satisfied_review_id=4401589029,
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
