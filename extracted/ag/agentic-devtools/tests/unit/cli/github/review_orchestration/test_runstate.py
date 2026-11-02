import json

import pytest
from pydantic import ValidationError

from agentic_devtools.cli.github.review_orchestration import RunState


def test_resume_identity_is_explicit(state_data):
    state = RunState.from_json(
        json.dumps(state_data), expected_pr_url=state_data["pr_url"], expected_run_id=state_data["run_id"]
    )
    assert state.run_id == state_data["run_id"]
    assert state.next_due_at == 1000
    assert state.findings[0].resources() == frozenset(
        {
            "file:src/example.py",
            "file:tests/test_example.py",
            "effect:branch-write",
        }
    )
    assert (
        RunState.from_json(
            state.model_dump_json(),
            expected_pr_url=state_data["pr_url"] + "#pullrequestreview-9",
            expected_run_id=state.run_id,
        )
        == state
    )


@pytest.mark.parametrize("raw", ["null", "[]", "{}", "{bad", '{"schema_version": 2}'])
def test_malformed_state_is_not_empty(raw, state_data):
    with pytest.raises(ValueError):
        RunState.from_json(raw, expected_pr_url=state_data["pr_url"], expected_run_id=state_data["run_id"])


@pytest.mark.parametrize(
    "field,value",
    [
        ("pr_url", "https://github.com/example/project/pull/8"),
        ("run_id", "00000000-0000-4000-8000-000000000002"),
    ],
)
def test_rejects_resume_target_mismatch(state_data, field, value):
    expected = {field: value}
    with pytest.raises(ValueError, match="resume identity"):
        RunState.from_json(
            json.dumps(state_data),
            expected_pr_url=expected.get("pr_url", state_data["pr_url"]),
            expected_run_id=expected.get("run_id", state_data["run_id"]),
        )


@pytest.mark.parametrize(
    "field,value",
    [
        ("schema_version", 2),
        ("schema_version", True),
        ("max_cycles", 0),
        ("max_cycles", 13),
        ("max_parallel", 0),
        ("cycles", -1),
        ("started_at", True),
        ("deadline_at", 1000),
        ("deadline_at", 4601),
        ("next_due_at", 999),
        ("next_due_at", 4601),
        ("authorized_actions", ["auto"]),
        ("run_id", "not-a-uuid"),
        ("review_requested_head", "short"),
        ("status", "ready"),
        ("pr_url", "https://github.com/example/project/pull/7#pullrequestreview-9"),
    ],
)
def test_rejects_invalid_contract(state_data, field, value):
    with pytest.raises(ValidationError):
        RunState.model_validate({**state_data, field: value})


def test_requires_explicit_completeness_and_unique_findings(state_data):
    del state_data["evidence"]["threads"]
    with pytest.raises(ValidationError):
        RunState.model_validate(state_data)
    state_data["evidence"]["threads"] = "unknown"
    assert RunState.model_validate(state_data).evidence.threads == "unknown"
    state_data["findings"].append(state_data["findings"][0].copy())
    with pytest.raises(ValidationError, match="duplicate finding"):
        RunState.model_validate(state_data)


def test_validates_reservation_ownership_and_resources(reserve):
    state_data = reserve()
    assert RunState.model_validate(state_data).reservations[0].attempt_id == "attempt-1"
    state_data["reservations"][0]["resources"] = ["file:other.py"]
    with pytest.raises(ValidationError, match="reservation"):
        RunState.model_validate(state_data)


@pytest.mark.parametrize(
    "change",
    [
        "missing",
        "unknown_finding",
        "wrong_attempt",
        "duplicate",
        "pending",
        "overlap",
        "duplicate_attempt",
        "duplicate_task",
        "duplicate_session",
    ],
)
def test_rejects_unsafe_leases(reserve, change):
    state_data = reserve()
    reservation = state_data["reservations"][0]
    if change == "missing":
        state_data["reservations"] = []
    elif change == "unknown_finding":
        reservation["finding_id"] = "f" * 64
    elif change == "wrong_attempt":
        reservation["attempt_id"] = "attempt-2"
    elif change == "duplicate":
        state_data["reservations"].append(reservation.copy())
    elif change == "pending":
        state_data["findings"][0].update(status="pending", attempt_id=None, task_id=None, session_id=None)
    elif change == "overlap":
        from agentic_devtools.cli.github.review_orchestration import Finding

        other = {
            **state_data["findings"][0],
            "comment_id": 24,
            "attempt_id": "attempt-2",
            "task_id": "task-2",
            "session_id": "session-2",
        }
        state_data["findings"].append(other)
        state_data["reservations"].append(
            {
                **reservation,
                "finding_id": Finding.model_validate(other).identity(state_data["pr_url"]),
                "attempt_id": "attempt-2",
            }
        )
    else:
        from agentic_devtools.cli.github.review_orchestration import Finding

        identity_field = {
            "duplicate_attempt": "attempt_id",
            "duplicate_task": "task_id",
            "duplicate_session": "session_id",
        }[change]
        other = {
            **state_data["findings"][0],
            "comment_id": 24,
            "path": "other.py",
            "attempt_id": "attempt-2",
            "task_id": "task-2",
            "session_id": "session-2",
        }
        other[identity_field] = state_data["findings"][0][identity_field]
        parsed = Finding.model_validate(other)
        state_data["findings"].append(other)
        state_data["reservations"].append(
            {
                "finding_id": parsed.identity(state_data["pr_url"]),
                "attempt_id": other["attempt_id"],
                "head_sha": "a" * 40,
                "resources": sorted(parsed.resources()),
            }
        )
    with pytest.raises(ValidationError, match="reservation|dispatch"):
        RunState.model_validate(state_data)


def test_duplicate_json_fields_cannot_reset_progress(state_data):
    raw = json.dumps(state_data).replace('"cycles": 0', '"cycles": 12, "cycles": 0')
    with pytest.raises(ValueError, match="duplicate JSON field"):
        RunState.from_json(raw, expected_pr_url=state_data["pr_url"], expected_run_id=state_data["run_id"])
