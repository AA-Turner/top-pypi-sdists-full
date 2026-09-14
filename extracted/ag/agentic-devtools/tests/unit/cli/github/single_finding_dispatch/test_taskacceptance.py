import pytest

from agentic_devtools.cli.github.single_finding_dispatch import (
    AcceptedTaskIdentity,
    TaskAcceptance,
)


def test_task_acceptance_requires_identity_for_accepted_tasks():
    accepted = TaskAcceptance("accepted", AcceptedTaskIdentity("task-1", "session-1"), "created")

    assert accepted.outcome == "accepted"
    assert accepted.identity is not None


@pytest.mark.parametrize(
    "outcome,identity",
    [
        ("accepted", None),
        ("already_resolved", AcceptedTaskIdentity("task-1", None)),
        ("head_changed", AcceptedTaskIdentity("task-1", None)),
        ("blocked", AcceptedTaskIdentity("task-1", None)),
        ("invalid", None),
    ],
)
def test_task_acceptance_rejects_invalid_outcomes(outcome, identity):
    with pytest.raises(ValueError):
        TaskAcceptance(outcome, identity, "reason")


def test_task_acceptance_requires_a_reason():
    with pytest.raises(ValueError, match="reason"):
        TaskAcceptance("head_changed", None, " ")


def test_task_acceptance_allows_already_resolved_without_identity():
    acceptance = TaskAcceptance("already_resolved", None, "thread was resolved")

    assert acceptance.outcome == "already_resolved"
    assert acceptance.identity is None


def test_task_acceptance_allows_blocked_without_identity():
    acceptance = TaskAcceptance("blocked", None, "thread lookup failed")

    assert acceptance.outcome == "blocked"
    assert acceptance.identity is None


def test_task_acceptance_rejects_an_untyped_identity():
    with pytest.raises(ValueError, match="AcceptedTaskIdentity"):
        TaskAcceptance("accepted", object(), "created")  # type: ignore[arg-type]
