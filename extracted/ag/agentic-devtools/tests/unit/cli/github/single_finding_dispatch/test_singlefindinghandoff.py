import pytest
from pydantic import ValidationError

from agentic_devtools.cli.github.review_orchestration import Finding
from agentic_devtools.cli.github.single_finding_dispatch import SingleFindingHandoff


def test_single_finding_handoff_requires_matching_branch_write_reservation(handoff_data):
    handoff = SingleFindingHandoff.model_validate(handoff_data)

    assert handoff.finding_id == handoff.finding.identity(handoff.pr_url)
    assert handoff.reservation.resources == ("effect:branch-write", "file:src/example.py")


@pytest.mark.parametrize(
    "updates",
    [
        {"expected_head": None},
        {"expected_head": "c" * 40},
        {"run_id": " "},
        {"run_id": "not-a-uuid"},
        {"deadline_at": 0},
        {"deadline_at": float("inf")},
        {
            "reservation": {
                "finding_id": "c" * 64,
                "attempt_id": "attempt-1",
                "head_sha": "a" * 40,
                "resources": ["effect:branch-write"],
            }
        },
        {
            "reservation": {
                "finding_id": "b" * 64,
                "attempt_id": "attempt-2",
                "head_sha": "a" * 40,
                "resources": ["effect:branch-write"],
            }
        },
        {
            "reservation": {
                "finding_id": "b" * 64,
                "attempt_id": "attempt-1",
                "head_sha": "c" * 40,
                "resources": ["effect:branch-write"],
            }
        },
        {
            "reservation": {
                "finding_id": "b" * 64,
                "attempt_id": "attempt-1",
                "head_sha": "a" * 40,
                "resources": ["file:src/example.py"],
            }
        },
        {"unrecognized": True},
        {"authorized_actions": []},
        {
            "remaining_failure_budgets": {
                "throttling": 3,
                "transport": 3,
                "credential": 1,
                "oauth": 1,
                "repair": 0,
            }
        },
        {"finding": {"status": "pending"}},
    ],
)
def test_single_finding_handoff_rejects_unsafe_contracts(handoff_data, updates):
    with pytest.raises(ValidationError):
        SingleFindingHandoff.model_validate({**handoff_data, **updates})


def test_single_finding_handoff_rejects_noncanonical_pr_url(handoff_data):
    with pytest.raises(ValidationError, match="canonical"):
        SingleFindingHandoff.model_validate({**handoff_data, "pr_url": "https://github.com/EXAMPLE/PROJECT/pull/7"})


@pytest.mark.parametrize(
    "finding_update",
    [
        {"thread_id": None},
        {"task_id": "task-1"},
        {"session_id": "session-1"},
    ],
)
def test_single_finding_handoff_requires_unassigned_assigned_thread(handoff_data, finding_update):
    finding = {**handoff_data["finding"], **finding_update}

    with pytest.raises(ValidationError, match="assigned thread|task or session"):
        SingleFindingHandoff.model_validate({**handoff_data, "finding": finding})


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("throttling", 0),
        ("throttling", 4),
        ("transport", 0),
        ("transport", 4),
        ("credential", 0),
        ("credential", 2),
        ("oauth", 0),
        ("oauth", 2),
        ("repair", 0),
        ("repair", 3),
    ],
)
def test_single_finding_handoff_rejects_exhausted_or_excessive_failure_budget(handoff_data, field, value):
    budgets = {**handoff_data["remaining_failure_budgets"], field: value}

    with pytest.raises(ValidationError, match=f"remaining {field} failure budget"):
        SingleFindingHandoff.model_validate({**handoff_data, "remaining_failure_budgets": budgets})


@pytest.mark.parametrize(
    ("field", "message"),
    [
        ("provenance", "finding provenance"),
        ("status", "finding must be reserved"),
        ("attempt", "finding attempt_id"),
        ("reservation_attempt", "reservation attempt_id"),
        ("resources", "reservation resources"),
        ("reservation_resource", "branch-write"),
        ("authorization", "repair action"),
        ("budget", "remaining repair"),
    ],
)
def test_single_finding_handoff_validates_dispatch_context(handoff_data, field, message):
    data = dict(handoff_data)
    finding = dict(data["finding"])
    reservation = dict(data["reservation"])
    if field == "provenance":
        finding["review_id"] = 4
    elif field == "status":
        finding["status"] = "blocked"
    elif field == "attempt":
        finding["attempt_id"] = "attempt-2"
    elif field == "reservation_attempt":
        reservation["attempt_id"] = "attempt-2"
    elif field == "resources":
        finding["path"] = "src/other.py"
        finding["side_effects"] = ()
        finding_model = Finding.model_validate(finding)
        data["finding_id"] = finding_model.identity(data["pr_url"])
        reservation["finding_id"] = data["finding_id"]
    elif field == "reservation_resource":
        reservation["resources"] = ["file:src/example.py"]
    elif field == "authorization":
        data["authorized_actions"] = []
    else:
        data["remaining_failure_budgets"] = {
            "throttling": 3,
            "transport": 3,
            "credential": 1,
            "oauth": 1,
            "repair": 0,
        }
    data["finding"] = finding
    data["reservation"] = reservation

    with pytest.raises(ValidationError, match=message):
        SingleFindingHandoff.model_validate(data)
