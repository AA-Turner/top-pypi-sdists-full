"""Tests for adjudicating critique-task outcomes."""

from dataclasses import replace
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.critique_adjudicator import (
    CritiqueAdjudication,
    CritiqueAdjudicationRecord,
)
from agentic_devtools.cli.ci.evaluator.critique_actions import adjudicate_critique
from agentic_devtools.cli.ci.evaluator.models import PostAgentSnapshot
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError
from tests.unit.cli.ci.evaluator.critique_actions._support import (
    _make_needs_repair_dispatch_case,
    _make_provider,
    _make_snapshot,
    _make_task,
)


def test_needs_repair_dispatch_uses_unpersisted_adjudication_before_marker_write() -> None:
    provider, comments, post_agent_snapshot, live_snapshot = _make_needs_repair_dispatch_case()

    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication",
            return_value=CritiqueAdjudication(
                verdict="needs_repair",
                rationale="A concrete parser regression remains.",
                concrete_instruction="Add a regression test for the parser boundary case.",
            ),
        ),
        patch("agentic_devtools.cli.ci.evaluator.critique_actions.build_pr_state_snapshot", return_value=live_snapshot),
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
            return_value=False,
        ),
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
            return_value=(False, 0),
        ),
    ):
        result = adjudicate_critique(provider, post_agent_snapshot)

    assert result.success is True
    assert provider.dispatch_repair.call_args.kwargs["agent_task_prompt"] == (
        "@copilot please address the following critique of this pr:\n\n"
        "Add a regression test for the parser boundary case."
    )
    assert any(
        "critique-adjudicated pr=42 head=head review=100 verdict=needs_repair" in comment.body
        for comment in comments.values()
    )


def test_missing_task_identity_returns_failure_without_provider_calls() -> None:
    provider = MagicMock()
    snapshot = _make_snapshot(task=None)
    snapshot = PostAgentSnapshot(pr_number=snapshot.pr_number, threads=snapshot.threads)

    result = adjudicate_critique(provider, snapshot)

    assert result.success is False
    assert result.threads_unresolved == 1
    assert result.error_details is not None and "identity is unavailable" in result.error_details
    provider.get_pr_metadata.assert_not_called()


@pytest.mark.parametrize(
    ("verdict", "expected_label_calls"),
    [("rebutted", 0), ("needs_repair", 0), ("needs_human", 1)],
)
def test_existing_adjudication_is_idempotent_and_restores_needs_human_label(
    verdict: str,
    expected_label_calls: int,
) -> None:
    task = _make_task()
    record = CritiqueAdjudicationRecord(42, "head", 100, 1, verdict, "Stored outcome.")
    provider = _make_provider("head")

    with patch("agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication") as run_ai:
        result = adjudicate_critique(provider, _make_snapshot(task=task, adjudications=(record,)))

    assert result.success is True
    assert result.threads_unresolved == 1
    assert provider.add_label.call_count == expected_label_calls
    assert provider.get_pr_metadata.call_count == expected_label_calls
    run_ai.assert_not_called()


@pytest.mark.parametrize(
    ("metadata_head", "snapshot_head"),
    [("new-head", "head"), ("head", "new-head")],
)
def test_existing_needs_human_does_not_restore_label_after_head_change(
    metadata_head: str,
    snapshot_head: str,
) -> None:
    task = _make_task()
    record = CritiqueAdjudicationRecord(42, "head", 100, 1, "needs_human", "Escalated.")
    provider = _make_provider(metadata_head)
    with patch("agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication") as run_ai:
        result = adjudicate_critique(
            provider,
            _make_snapshot(task=task, adjudications=(record,), current_head_sha=snapshot_head),
        )

    assert result.success is True
    assert result.error_details is not None and "stale HEAD" in result.error_details
    provider.get_pr_metadata.assert_called_once()
    provider.add_label.assert_not_called()
    provider.post_comment.assert_not_called()
    provider.post_comment_as_pr_token.assert_not_called()
    provider.update_comment.assert_not_called()
    provider.update_comment_as_pr_token.assert_not_called()
    run_ai.assert_not_called()


def test_existing_needs_human_does_not_restore_label_when_head_is_unavailable() -> None:
    task = _make_task()
    record = CritiqueAdjudicationRecord(42, "head", 100, 1, "needs_human", "Escalated.")
    provider = MagicMock()
    provider.get_pr_metadata.side_effect = RuntimeError("provider unavailable")
    with patch("agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication") as run_ai:
        result = adjudicate_critique(provider, _make_snapshot(task=task, adjudications=(record,)))

    assert result.success is False
    assert result.error_details is not None and "before adjudication" in result.error_details
    provider.get_pr_metadata.assert_called_once()
    provider.add_label.assert_not_called()
    provider.post_comment.assert_not_called()
    provider.post_comment_as_pr_token.assert_not_called()
    provider.update_comment.assert_not_called()
    provider.update_comment_as_pr_token.assert_not_called()
    run_ai.assert_not_called()


def test_dry_run_existing_needs_human_does_not_verify_or_restore_label() -> None:
    task = _make_task()
    record = CritiqueAdjudicationRecord(42, "head", 100, 1, "needs_human", "Escalated.")
    provider = MagicMock()
    with patch("agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication") as run_ai:
        result = adjudicate_critique(
            provider,
            _make_snapshot(task=task, adjudications=(record,)),
            dry_run=True,
        )

    assert result.success is True
    assert result.dry_run is True
    provider.get_pr_metadata.assert_not_called()
    provider.add_label.assert_not_called()
    provider.post_comment_as_pr_token.assert_not_called()
    run_ai.assert_not_called()


def test_dry_run_does_not_call_ai_or_persist_an_adjudication() -> None:
    provider = MagicMock()
    with patch("agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication") as run_ai:
        result = adjudicate_critique(provider, _make_snapshot(), dry_run=True)

    assert result.success is True
    assert result.dry_run is True
    run_ai.assert_not_called()
    provider.get_pr_metadata.assert_not_called()


def test_existing_needs_human_adjudication_restores_label_failure() -> None:
    task = _make_task()
    record = CritiqueAdjudicationRecord(42, "head", 100, 1, "needs_human", "Escalated.")
    provider = _make_provider("head")
    provider.add_label.side_effect = RuntimeError("label unavailable")

    result = adjudicate_critique(provider, _make_snapshot(task=task, adjudications=(record,)))

    assert result.success is False
    assert result.error_details is not None and "could not be restored" in result.error_details


def test_unavailable_initial_head_verification_returns_failure() -> None:
    provider = MagicMock()
    provider.get_pr_metadata.side_effect = RuntimeError("provider unavailable")

    result = adjudicate_critique(provider, _make_snapshot())

    assert result.success is False
    assert result.error_details is not None and "before adjudication" in result.error_details


@pytest.mark.parametrize(
    ("current_metadata_head", "snapshot_head"),
    [("other-head", "head"), ("head", "other-head")],
)
def test_stale_task_head_is_not_adjudicated(current_metadata_head: str, snapshot_head: str) -> None:
    provider = _make_provider(current_metadata_head)
    with patch("agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication") as run_ai:
        result = adjudicate_critique(provider, _make_snapshot(current_head_sha=snapshot_head))

    assert result.success is True
    assert result.error_details is not None and "stale HEAD" in result.error_details
    run_ai.assert_not_called()


def test_ai_failure_is_persisted_as_needs_human_and_labeled() -> None:
    provider = _make_provider("head", "head")
    with patch(
        "agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication",
        side_effect=RuntimeError("malformed response"),
    ):
        result = adjudicate_critique(provider, _make_snapshot())

    assert result.success is True
    assert "verdict=needs_human" in provider.post_comment_as_pr_token.call_args.args[1]
    provider.add_label.assert_called_once()


def test_lock_loss_after_ai_adjudication_prevents_mutations() -> None:
    provider, owns_lock = _make_provider("head"), MagicMock(side_effect=[True, False])
    with patch(
        "agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication", side_effect=RuntimeError
    ):
        assert not adjudicate_critique(provider, _make_snapshot(), ownership_guard=owns_lock).success
    provider.post_comment_as_pr_token.assert_not_called()


def test_two_attempts_exhausted_escalates_needs_repair_to_needs_human() -> None:
    provider = _make_provider("head", "head")
    tasks = (_make_task(1), _make_task(2))
    live_snapshot = PRStateSnapshot(pr_number=42, head_sha="head")
    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication",
            return_value=CritiqueAdjudication(
                verdict="needs_repair",
                rationale="A concrete defect remains.",
                concrete_instruction="Repair the defect.",
            ),
        ),
        patch("agentic_devtools.cli.ci.evaluator.critique_actions.build_pr_state_snapshot", return_value=live_snapshot),
    ):
        result = adjudicate_critique(provider, _make_snapshot(tasks=tasks))

    assert result.success is True
    assert "verdict=needs_human" in provider.post_comment_as_pr_token.call_args.args[1]
    provider.add_label.assert_called_once()


def test_failed_adjudication_marker_after_dispatch_cannot_exceed_head_attempt_cap() -> None:
    repair = CritiqueAdjudication(
        verdict="needs_repair",
        rationale="A concrete defect remains.",
        concrete_instruction="Repair the defect.",
    )
    first_provider = _make_provider("head", "head")
    first_provider.post_comment_as_pr_token.side_effect = RuntimeError("comment write failed")
    with (
        patch("agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication", return_value=repair),
        patch(
            "agentic_devtools.cli.ci.evaluator.critique_actions._dispatch_followup",
            return_value=(repair, None),
        ) as dispatch_followup,
    ):
        first_result = adjudicate_critique(first_provider, _make_snapshot())

    assert first_result.success is False
    assert first_result.error_details is not None and "marker write failed" in first_result.error_details
    dispatch_followup.assert_called_once()

    second_provider = _make_provider("head", "head")
    with (
        patch("agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication", return_value=repair),
        patch(
            "agentic_devtools.cli.ci.evaluator.critique_actions._dispatch_followup",
            return_value=(repair, None),
        ) as second_dispatch,
    ):
        second_result = adjudicate_critique(
            second_provider,
            _make_snapshot(task=_make_task(2), tasks=(_make_task(1), _make_task(2))),
        )

    assert second_result.success is True
    assert "verdict=needs_human" in second_provider.post_comment_as_pr_token.call_args.args[1]
    second_provider.add_label.assert_called_once()
    second_dispatch.assert_not_called()


def test_head_change_before_follow_up_dispatch_stops_without_persisting() -> None:
    provider = _make_provider("head")
    live_snapshot = PRStateSnapshot(pr_number=42, head_sha="new-head")
    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication",
            return_value=CritiqueAdjudication(
                verdict="needs_repair",
                rationale="A concrete defect remains.",
                concrete_instruction="Repair the defect.",
            ),
        ),
        patch(
            "agentic_devtools.cli.ci.evaluator.critique_actions.build_pr_state_snapshot",
            return_value=live_snapshot,
        ),
    ):
        result = adjudicate_critique(provider, _make_snapshot())

    assert result.success is True
    assert result.error_details is not None and "HEAD changed before" in result.error_details
    provider.post_comment_as_pr_token.assert_not_called()


@pytest.mark.parametrize("changed_context", ["review_id", "headline"])
def test_changed_live_review_context_defers_follow_up_dispatch(changed_context: str) -> None:
    provider, _comments, post_agent_snapshot, live_snapshot = _make_needs_repair_dispatch_case()
    review = live_snapshot.reviews[0]
    verdict = live_snapshot.copilot_gate_verdict
    assert verdict is not None
    if changed_context == "review_id":
        changed_review = replace(review, id=101)
        live_snapshot = replace(
            live_snapshot,
            copilot_review_id=101,
            effective_review_comment_count_review_id=101,
            copilot_gate_verdict=replace(verdict, review_id=101),
            reviews=[changed_review],
        )
    else:
        changed_headline = "A newer parser defect needs a targeted repair."
        changed_body = f"<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n{changed_headline}\n\n0 open findings"
        live_snapshot = replace(live_snapshot, reviews=[replace(review, body=changed_body)])

    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication",
            return_value=CritiqueAdjudication(
                verdict="needs_repair",
                rationale="A concrete parser regression remains.",
                concrete_instruction="Repair the parser boundary case.",
            ),
        ),
        patch(
            "agentic_devtools.cli.ci.evaluator.critique_actions.build_pr_state_snapshot",
            return_value=live_snapshot,
        ),
    ):
        result = adjudicate_critique(provider, post_agent_snapshot)

    assert result.success is True
    assert result.error_details is not None and "review context changed" in result.error_details
    provider.dispatch_repair.assert_not_called()
    provider.post_comment_as_pr_token.assert_not_called()


@pytest.mark.parametrize("dispatch_stage", ["preflight", "execute", "already_dispatched", "completed"])
def test_failed_follow_up_dispatch_escalates_or_records_created_task(dispatch_stage: str) -> None:
    provider = _make_provider("head", "head")
    _, _, post_agent_snapshot, live_snapshot = _make_needs_repair_dispatch_case()

    class FakeDispatch:
        def evaluate(self, _snapshot, _derived):
            decision = ActionDecision.SKIP if dispatch_stage == "preflight" else ActionDecision.EXECUTE
            return ActionResult(name="dispatch", decision=decision, details="preflight denied")

        def execute(self, _provider, _snapshot, derived):
            if dispatch_stage == "already_dispatched":
                derived.set("repair_dispatched", True)
            if dispatch_stage == "completed":
                return ActionResult(name="dispatch", decision=ActionDecision.EXECUTE, details="dispatch complete")
            if dispatch_stage == "execute":
                return ActionResult(name="dispatch", decision=ActionDecision.SKIP, details="dispatch denied")
            return ActionResult(name="dispatch", decision=ActionDecision.SKIP, details="bookkeeping interrupted")

    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication",
            return_value=CritiqueAdjudication(
                verdict="needs_repair",
                rationale="A concrete defect remains.",
                concrete_instruction="Repair the defect.",
            ),
        ),
        patch("agentic_devtools.cli.ci.evaluator.critique_actions.build_pr_state_snapshot", return_value=live_snapshot),
        patch("agentic_devtools.cli.ci.evaluator.critique_actions.DispatchRepairAction", FakeDispatch),
    ):
        result = adjudicate_critique(provider, post_agent_snapshot)

    assert result.success is True
    expected_verdict = "needs_repair" if dispatch_stage in {"already_dispatched", "completed"} else "needs_human"
    assert f"verdict={expected_verdict}" in provider.post_comment_as_pr_token.call_args.args[1]
    assert provider.add_label.call_count == (0 if expected_verdict == "needs_repair" else 1)


@pytest.mark.parametrize(
    ("error", "propagates"),
    [
        (RuntimeError("snapshot unavailable"), False),
        (ProviderRateLimitError(provider="github", is_rate_limit=False), False),
        (ProviderRateLimitError(provider="github", is_rate_limit=True), True),
    ],
)
def test_follow_up_snapshot_errors_escalate_or_propagate(error: Exception, propagates: bool) -> None:
    provider = _make_provider("head", "head")
    with (
        patch(
            "agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication",
            return_value=CritiqueAdjudication(
                verdict="needs_repair",
                rationale="A concrete defect remains.",
                concrete_instruction="Repair the defect.",
            ),
        ),
        patch(
            "agentic_devtools.cli.ci.evaluator.critique_actions.build_pr_state_snapshot",
            side_effect=error,
        ),
    ):
        if propagates:
            with pytest.raises(ProviderRateLimitError) as exc_info:
                adjudicate_critique(provider, _make_snapshot())
            assert exc_info.value is error
            provider.post_comment_as_pr_token.assert_not_called()
            provider.add_label.assert_not_called()
        else:
            result = adjudicate_critique(provider, _make_snapshot())
            assert result.success is True
            assert "verdict=needs_human" in provider.post_comment_as_pr_token.call_args.args[1]
            provider.add_label.assert_called_once()


def test_unavailable_final_head_verification_does_not_persist_outcome() -> None:
    provider = _make_provider("head")
    provider.get_pr_metadata.side_effect = [
        SimpleNamespace(head_sha="head"),
        RuntimeError("provider unavailable"),
    ]
    with patch(
        "agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication",
        return_value=CritiqueAdjudication(verdict="rebutted", rationale="No code defect was found."),
    ):
        result = adjudicate_critique(provider, _make_snapshot())

    assert result.success is False
    assert result.error_details is not None and "before persisting" in result.error_details
    provider.post_comment_as_pr_token.assert_not_called()


def test_head_change_before_final_persistence_discards_adjudication() -> None:
    provider = _make_provider("head", "new-head")
    with patch(
        "agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication",
        return_value=CritiqueAdjudication(verdict="rebutted", rationale="No code defect was found."),
    ):
        result = adjudicate_critique(provider, _make_snapshot())

    assert result.success is True
    assert result.error_details is not None and "HEAD changed before" in result.error_details
    provider.post_comment_as_pr_token.assert_not_called()


@pytest.mark.parametrize("failure", ["exception", "invalid_id"])
def test_adjudication_marker_write_failure_returns_failure(failure: str) -> None:
    provider = _make_provider("head", "head")
    if failure == "exception":
        provider.post_comment_as_pr_token.side_effect = RuntimeError("comment unavailable")
    else:
        provider.post_comment_as_pr_token.return_value = 0
    with patch(
        "agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication",
        return_value=CritiqueAdjudication(verdict="rebutted", rationale="No code defect was found."),
    ):
        result = adjudicate_critique(provider, _make_snapshot())

    assert result.success is False
    assert result.error_details is not None and "marker write failed" in result.error_details


def test_needs_human_label_failure_reports_persisted_outcome() -> None:
    provider = _make_provider("head", "head")
    provider.add_label.side_effect = RuntimeError("label unavailable")
    with patch(
        "agentic_devtools.cli.ci.evaluator.critique_actions.run_critique_adjudication",
        return_value=CritiqueAdjudication(verdict="needs_human", rationale="A human decision is required."),
    ):
        result = adjudicate_critique(provider, _make_snapshot())

    assert result.success is False
    assert result.error_details is not None and "outcome persisted but label write failed" in result.error_details
