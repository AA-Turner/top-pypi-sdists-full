from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.reconciliation.models import QueueState, WorkItem, WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.supervisor import (
    IncidentManager,
    RecoveryActionType,
    StaleProposalError,
    SupervisorGovernor,
    SupervisorProposal,
    evaluate_supervisor_proposal,
    proposal_from_dict,
    propose_controller_repair,
)


def _state(*, work: bool) -> QueueState:
    items = {1: WorkItem(1, "o/r", "c", "pending", None, WorkItemStatus.QUEUED)} if work else {}
    return QueueState("o/r", 0, items, [], [])


def _proposal() -> SupervisorProposal:
    return SupervisorProposal("p", RecoveryActionType.RETRY_WITH_REDUCED_SCOPE, "o/r", 1, "ob", "head", "problem")


def test_governor_gate_and_limits() -> None:
    now = datetime(2026, 1, 1, tzinfo=UTC)
    governor = SupervisorGovernor()
    assert tuple(governor.should_run(_state(work=False), now)) == (False, "no work exists")
    decision = governor.should_run(_state(work=True), now)
    assert decision.allowed
    assert bool(decision)
    governor.record_execution(now)
    assert governor.should_run(_state(work=True), now + timedelta(minutes=30)).reason == "hourly limit reached"
    for index in range(23):
        governor.record_execution(now + timedelta(hours=index + 1))
    assert governor.should_run(_state(work=True), now + timedelta(hours=23, minutes=1)).reason == "daily limit reached"


def test_governor_validation() -> None:
    with pytest.raises(ValueError):
        SupervisorGovernor(hourly_interval_seconds=1)
    with pytest.raises(ValueError):
        SupervisorGovernor(daily_limit=0)
    with pytest.raises(ValueError):
        SupervisorGovernor().should_run(_state(work=True), datetime.now())
    with pytest.raises(ValueError):
        SupervisorGovernor().record_execution(datetime.now())


def test_proposal_evaluation() -> None:
    proposal = _proposal()
    assert evaluate_supervisor_proposal(proposal, current_head_sha="head").accepted
    assert (
        evaluate_supervisor_proposal(proposal, current_head_sha="head", applied_proposal_ids={"p"}).status
        == "already_settled"
    )
    assert (
        evaluate_supervisor_proposal(
            proposal, current_head_sha="head", applied_actions={"o/r|1|ob|problem|retry_with_reduced_scope"}
        ).status
        == "already_settled"
    )
    assert evaluate_supervisor_proposal(proposal, current_head_sha="head", attempt_count=3).status == "rejected"
    assert evaluate_supervisor_proposal(proposal, current_head_sha="head", round_count=50).status == "rejected"
    with pytest.raises(StaleProposalError):
        evaluate_supervisor_proposal(proposal, current_head_sha="other")


def test_incident_deduplication_and_remediation() -> None:
    with pytest.raises(ValueError):
        IncidentManager(round_limit=0)
    manager = IncidentManager()
    first = manager.get_or_create("capacity", "provider-x")
    assert manager.get_or_create("capacity", "provider-x").incident_id == first.incident_id
    manager.attach(first.incident_id, "a")
    manager.attach(first.incident_id, "b")
    manager.mark_remediated(first.incident_id)
    assert manager.grant_extra_luna(first.incident_id, "a", rounds_used=49)
    assert not manager.grant_extra_luna(first.incident_id, "a", rounds_used=49)
    assert not manager.grant_extra_luna(first.incident_id, "b", rounds_used=50)
    assert not manager.grant_extra_luna(first.incident_id, "missing", rounds_used=1)
    assert len(manager.incidents()) == 1


def test_controller_repair_and_parsing() -> None:
    repair = propose_controller_repair(
        repo="o/r", pr_number=1, obligation_id="ob", target_head_sha="h", issue_key="#4005", defect="controller defect"
    )
    assert repair.action is RecoveryActionType.PROPOSE_CONTROLLER_REPAIR
    parsed = proposal_from_dict(
        {
            "action": repair.action.value,
            "proposal_id": "p",
            "repo": "o/r",
            "pr_number": 1,
            "obligation_id": "ob",
            "target_head_sha": "h",
            "problem_hash": "x",
        }
    )
    assert parsed.pr_number == 1
    with pytest.raises(ValueError):
        propose_controller_repair(
            repo="o/r", pr_number=1, obligation_id="ob", target_head_sha="h", issue_key="", defect="x"
        )
    with pytest.raises((TypeError, ValueError)):
        proposal_from_dict({"action": "bad"})
    with pytest.raises(TypeError):
        proposal_from_dict("bad")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        proposal_from_dict(
            {
                "action": repair.action.value,
                "proposal_id": "p",
                "repo": "o/r",
                "pr_number": "1",
                "obligation_id": "ob",
                "target_head_sha": "h",
                "problem_hash": "x",
            }
        )
