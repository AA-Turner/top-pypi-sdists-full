"""Regression coverage for publication eligibility through the public action."""

from unittest.mock import Mock

import pytest

import agentic_devtools.cli.ci.pipeline.actions.publish as publish_module
from agentic_devtools.cli.ci.pipeline.delivery import InitialDeliveryOutcome
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot


def _snapshot(*, title: str = "Ready for review") -> PRStateSnapshot:
    return PRStateSnapshot(
        pr_number=42,
        base_branch="main",
        head_branch="feature",
        is_draft=True,
        title=title,
        has_changes=True,
        base_repo_full_name="owner/repo",
        head_sha="head-sha",
    )


def test_changed_draft_is_eligible_for_publication(monkeypatch: pytest.MonkeyPatch) -> None:
    snapshot = _snapshot()
    monkeypatch.setattr(publish_module, "is_copilot_session_active_via_agent_task", Mock(return_value=False))

    result = publish_module.PublishAction().evaluate(snapshot, DerivedState(snapshot))

    assert result == ActionResult(
        name="publish",
        decision=ActionDecision.EXECUTE,
        preconditions={
            "is_draft": True,
            "has_changes": True,
            "not_wip": True,
            "no_active_session": True,
        },
        details="Draft PR ready to publish",
    )


def test_wip_title_without_confirmed_delivery_is_blocked(monkeypatch: pytest.MonkeyPatch) -> None:
    snapshot = _snapshot(title="[WIP] unfinished work")
    derived = DerivedState(snapshot)
    classify_delivery = Mock(return_value=InitialDeliveryOutcome.UNKNOWN)
    monkeypatch.setattr(publish_module, "classify_initial_delivery", classify_delivery)

    result = publish_module.PublishAction().evaluate(snapshot, derived)

    classify_delivery.assert_called_once_with(
        None,
        snapshot.pr_number,
        completion_confirmed=False,
        initial_plan_sha=None,
    )
    assert result == ActionResult(
        name="publish",
        decision=ActionDecision.SKIP,
        preconditions={"is_draft": True, "has_changes": True, "not_wip": False},
        details="PR title is WIP",
    )


def test_confirmed_initial_delivery_allows_wip_draft(monkeypatch: pytest.MonkeyPatch) -> None:
    snapshot = _snapshot(title="[WIP] completed work")
    derived = DerivedState(snapshot)
    derived.set("latest_session_state", SessionState(SessionOutcome.FINISHED))
    classify_delivery = Mock(return_value=InitialDeliveryOutcome.DELIVERED)
    monkeypatch.setattr(publish_module, "classify_initial_delivery", classify_delivery)
    monkeypatch.setattr(publish_module, "is_copilot_session_active_via_agent_task", Mock(return_value=False))

    result = publish_module.PublishAction().evaluate(snapshot, derived)

    classify_delivery.assert_called_once_with(
        None,
        snapshot.pr_number,
        completion_confirmed=True,
        initial_plan_sha=None,
    )
    assert result == ActionResult(
        name="publish",
        decision=ActionDecision.EXECUTE,
        preconditions={
            "is_draft": True,
            "has_changes": True,
            "not_wip": True,
            "no_active_session": True,
        },
        details="Draft PR ready to publish",
    )


@pytest.mark.parametrize("writer_state", [True, None], ids=["active-writer", "unknown-writer"])
def test_active_or_unknown_writer_blocks_publication(
    monkeypatch: pytest.MonkeyPatch,
    writer_state: bool | None,
) -> None:
    snapshot = _snapshot()
    monkeypatch.setattr(
        publish_module,
        "is_copilot_session_active_via_agent_task",
        Mock(return_value=writer_state),
    )

    result = publish_module.PublishAction().evaluate(snapshot, DerivedState(snapshot))

    assert result == ActionResult(
        name="publish",
        decision=ActionDecision.SKIP,
        preconditions={
            "is_draft": True,
            "has_changes": True,
            "not_wip": True,
            "no_active_session": False,
        },
        details="Copilot session active or inventory unavailable — publish blocked",
    )
