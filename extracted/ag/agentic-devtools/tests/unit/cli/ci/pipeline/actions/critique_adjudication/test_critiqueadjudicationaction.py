"""Tests for live-pipeline critique adjudication."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.critique_adjudicator import CritiqueTask
from agentic_devtools.cli.ci.evaluator.lock import LockStatus
from agentic_devtools.cli.ci.evaluator.models import (
    CommentInfo,
    EvaluationResult,
    PostAgentAction,
    PostAgentClassification,
    PostAgentSnapshot,
)
from agentic_devtools.cli.ci.pipeline.actions.critique_adjudication import CritiqueAdjudicationAction
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def _pipeline_snapshot() -> PRStateSnapshot:
    return PRStateSnapshot(pr_number=42, head_sha="head", base_repo_full_name="owner/repo")


def _post_agent_snapshot(
    *,
    reply_created_at: str = "2026-10-20T08:01:00Z",
    task_completed: bool | None = True,
) -> PostAgentSnapshot:
    return PostAgentSnapshot(
        pr_number=42,
        current_head_sha="head",
        review_id=100,
        critique_task=CritiqueTask(42, "head", 100, 1, "2026-10-20T08:00:00Z", "task-123"),
        critique_task_completed=task_completed,
        latest_agent_comment=CommentInfo(
            id=11,
            author="copilot-swe-agent[bot]",
            body="No changes were made.",
            created_at=reply_created_at,
        ),
    )


def _derived() -> DerivedState:
    snapshot = _pipeline_snapshot()
    derived = DerivedState(snapshot)
    derived.set("provider", MagicMock())
    return derived


def test_evaluate_requires_pipeline_lock_token_and_provider() -> None:
    action = CritiqueAdjudicationAction("")
    result = action.evaluate(_pipeline_snapshot(), _derived())
    assert result.decision is ActionDecision.BLOCKED

    action = CritiqueAdjudicationAction("token")
    derived = DerivedState(_pipeline_snapshot())
    result = action.evaluate(_pipeline_snapshot(), derived)
    assert result.decision is ActionDecision.BLOCKED


@pytest.mark.parametrize(
    "lock_status",
    [
        LockStatus(),
        LockStatus(is_locked=True, holder="another-run"),
        LockStatus(is_locked=True, holder="token", is_stale=True),
    ],
)
def test_evaluate_blocks_without_current_evaluator_lock(lock_status: LockStatus) -> None:
    action = CritiqueAdjudicationAction("token")
    with patch("agentic_devtools.cli.ci.evaluator.lock.check_lock_status", return_value=lock_status):
        result = action.evaluate(_pipeline_snapshot(), _derived())

    assert result.decision is ActionDecision.BLOCKED


def test_evaluate_blocks_when_lock_lookup_fails() -> None:
    action = CritiqueAdjudicationAction("token")
    with patch(
        "agentic_devtools.cli.ci.evaluator.lock.check_lock_status",
        side_effect=RuntimeError("lock lookup failed"),
    ):
        result = action.evaluate(_pipeline_snapshot(), _derived())

    assert result.decision is ActionDecision.BLOCKED


def test_evaluate_blocks_when_task_snapshot_cannot_be_built() -> None:
    action = CritiqueAdjudicationAction("token")
    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.lock.check_lock_status",
            return_value=LockStatus(is_locked=True, holder="token"),
        ),
        patch(
            "agentic_devtools.cli.ci.evaluator.snapshot_builder.build_snapshot",
            side_effect=RuntimeError("snapshot unavailable"),
        ),
    ):
        result = action.evaluate(_pipeline_snapshot(), _derived())

    assert result.decision is ActionDecision.BLOCKED


@pytest.mark.parametrize("failure_source", ["lock", "snapshot"])
@pytest.mark.parametrize("is_rate_limit", [True, False])
def test_evaluate_propagates_rate_limit_errors(failure_source: str, is_rate_limit: bool) -> None:
    action = CritiqueAdjudicationAction("token")
    rate_limit_error = ProviderRateLimitError(provider="github", is_rate_limit=is_rate_limit)
    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.lock.check_lock_status",
            side_effect=rate_limit_error if failure_source == "lock" else None,
            return_value=LockStatus(is_locked=True, holder="token"),
        ),
        patch(
            "agentic_devtools.cli.ci.evaluator.snapshot_builder.build_snapshot",
            side_effect=rate_limit_error if failure_source == "snapshot" else None,
        ),
    ):
        if is_rate_limit:
            with pytest.raises(ProviderRateLimitError) as exc_info:
                action.evaluate(_pipeline_snapshot(), _derived())
            assert exc_info.value is rate_limit_error
        else:
            result = action.evaluate(_pipeline_snapshot(), _derived())
            assert result.decision is ActionDecision.BLOCKED


def test_evaluate_skips_when_critique_task_has_no_completed_reply() -> None:
    action = CritiqueAdjudicationAction("token")
    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.lock.check_lock_status",
            return_value=LockStatus(is_locked=True, holder="token"),
        ),
        patch(
            "agentic_devtools.cli.ci.evaluator.snapshot_builder.build_snapshot",
            return_value=_post_agent_snapshot(reply_created_at="2026-10-20T07:59:00Z"),
        ),
    ):
        result = action.evaluate(_pipeline_snapshot(), _derived())

    assert result.decision is ActionDecision.SKIP


@pytest.mark.parametrize("success", [True, False])
def test_live_pipeline_adjudicates_completed_critique_task(success: bool) -> None:
    action = CritiqueAdjudicationAction("token")
    derived = _derived()
    evaluation = EvaluationResult(
        classification=PostAgentClassification.critique_adjudication,
        action_taken=PostAgentAction.adjudicate_critique,
        success=success,
        error_details=None if success else "adjudication failed",
    )
    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.lock.check_lock_status",
            return_value=LockStatus(is_locked=True, holder="token"),
        ),
        patch(
            "agentic_devtools.cli.ci.evaluator.snapshot_builder.build_snapshot",
            return_value=_post_agent_snapshot(),
        ) as build_snapshot,
        patch(
            "agentic_devtools.cli.ci.evaluator.critique_actions.adjudicate_critique",
            return_value=evaluation,
        ) as adjudicate,
    ):
        eligible = action.evaluate(_pipeline_snapshot(), derived)
        result = action.execute(derived.get("provider"), _pipeline_snapshot(), derived)
        assert callable(adjudicate.call_args.kwargs["ownership_guard"])
        assert adjudicate.call_args.kwargs["ownership_guard"]() is True

    assert eligible.decision is ActionDecision.EXECUTE
    assert build_snapshot.call_args.kwargs["current_lock_token"] == "token"
    adjudicate.assert_called_once()
    assert result.decision == (ActionDecision.EXECUTE if success else ActionDecision.FAILED)


def test_execute_blocks_when_evaluator_lock_changes_after_snapshot_revalidation() -> None:
    action = CritiqueAdjudicationAction("token")
    derived = _derived()
    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.lock.check_lock_status",
            side_effect=[
                LockStatus(is_locked=True, holder="token"),
                LockStatus(is_locked=True, holder="token"),
                LockStatus(),
            ],
        ),
        patch(
            "agentic_devtools.cli.ci.evaluator.snapshot_builder.build_snapshot",
            side_effect=[_post_agent_snapshot(), _post_agent_snapshot()],
        ),
        patch("agentic_devtools.cli.ci.evaluator.critique_actions.adjudicate_critique") as adjudicate,
    ):
        eligible = action.evaluate(_pipeline_snapshot(), derived)
        result = action.execute(derived.get("provider"), _pipeline_snapshot(), derived)

    assert eligible.decision is ActionDecision.EXECUTE
    assert result.decision is ActionDecision.BLOCKED
    adjudicate.assert_not_called()


def test_execute_blocks_when_evaluator_lock_changes_before_snapshot_revalidation() -> None:
    action = CritiqueAdjudicationAction("token")
    derived = _derived()
    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.lock.check_lock_status",
            side_effect=[LockStatus(is_locked=True, holder="token"), LockStatus()],
        ),
        patch(
            "agentic_devtools.cli.ci.evaluator.snapshot_builder.build_snapshot",
            return_value=_post_agent_snapshot(),
        ) as build_snapshot,
        patch("agentic_devtools.cli.ci.evaluator.critique_actions.adjudicate_critique") as adjudicate,
    ):
        eligible = action.evaluate(_pipeline_snapshot(), derived)
        result = action.execute(derived.get("provider"), _pipeline_snapshot(), derived)

    assert eligible.decision is ActionDecision.EXECUTE
    assert result.decision is ActionDecision.BLOCKED
    build_snapshot.assert_called_once()
    adjudicate.assert_not_called()


def test_execute_skips_when_task_becomes_active_after_evaluation() -> None:
    action = CritiqueAdjudicationAction("token")
    derived = _derived()
    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.lock.check_lock_status",
            return_value=LockStatus(is_locked=True, holder="token"),
        ),
        patch(
            "agentic_devtools.cli.ci.evaluator.snapshot_builder.build_snapshot",
            side_effect=[_post_agent_snapshot(), _post_agent_snapshot(task_completed=False)],
        ),
        patch("agentic_devtools.cli.ci.evaluator.critique_actions.adjudicate_critique") as adjudicate,
    ):
        eligible = action.evaluate(_pipeline_snapshot(), derived)
        result = action.execute(derived.get("provider"), _pipeline_snapshot(), derived)

    assert eligible.decision is ActionDecision.EXECUTE
    assert result.decision is ActionDecision.SKIP
    adjudicate.assert_not_called()


def test_execute_blocks_when_task_completion_cannot_be_reverified() -> None:
    action = CritiqueAdjudicationAction("token")
    derived = _derived()
    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.lock.check_lock_status",
            return_value=LockStatus(is_locked=True, holder="token"),
        ),
        patch(
            "agentic_devtools.cli.ci.evaluator.snapshot_builder.build_snapshot",
            side_effect=[_post_agent_snapshot(), RuntimeError("inventory unavailable")],
        ),
        patch("agentic_devtools.cli.ci.evaluator.critique_actions.adjudicate_critique") as adjudicate,
    ):
        eligible = action.evaluate(_pipeline_snapshot(), derived)
        result = action.execute(derived.get("provider"), _pipeline_snapshot(), derived)

    assert eligible.decision is ActionDecision.EXECUTE
    assert result.decision is ActionDecision.BLOCKED
    assert result.error == "inventory unavailable"
    adjudicate.assert_not_called()


@pytest.mark.parametrize("is_rate_limit", [True, False])
def test_execute_propagates_rate_limit_when_snapshot_cannot_be_reverified(is_rate_limit: bool) -> None:
    action = CritiqueAdjudicationAction("token")
    action._snapshot = _post_agent_snapshot()
    rate_limit_error = ProviderRateLimitError(provider="github", is_rate_limit=is_rate_limit)
    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.lock.check_lock_status",
            return_value=LockStatus(is_locked=True, holder="token"),
        ),
        patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.build_snapshot", side_effect=rate_limit_error),
    ):
        if is_rate_limit:
            with pytest.raises(ProviderRateLimitError) as exc_info:
                action.execute(_derived().get("provider"), _pipeline_snapshot(), _derived())
            assert exc_info.value is rate_limit_error
        else:
            result = action.execute(_derived().get("provider"), _pipeline_snapshot(), _derived())
            assert result.decision is ActionDecision.BLOCKED


def test_execute_skips_without_previously_verified_task_snapshot() -> None:
    action = CritiqueAdjudicationAction("token")

    result = action.execute(MagicMock(), _pipeline_snapshot(), _derived())

    assert result.decision is ActionDecision.SKIP
