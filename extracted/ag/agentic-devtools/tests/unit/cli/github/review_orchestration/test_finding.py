import pytest
from pydantic import ValidationError

from agentic_devtools.cli.github.review_orchestration import Finding


def test_inline_identity_ignores_position_and_task_progress(finding_data):
    original = Finding.model_validate(finding_data).identity("https://github.com/example/project/pull/7")
    finding_data.update(path="moved.py", thread_id="PRRT_other", status="resolved")
    assert Finding.model_validate(finding_data).identity("https://github.com/EXAMPLE/PROJECT/pull/7") == original
    finding_data["comment_id"] += 1
    assert Finding.model_validate(finding_data).identity("https://github.com/example/project/pull/7") != original


def test_suppressed_identity_survives_order_line_endings_and_synthetic_thread(finding_data):
    finding_data.update(comment_id=None, suppressed_body=" Concern\r\n  code\n", thread_id=None)
    finding = Finding.model_validate(finding_data)
    original = finding.identity("https://github.com/example/project/pull/7")
    finding_data.update(suppressed_body=" Concern\n  code\n", thread_id="PRRT_synthetic")
    assert Finding.model_validate(finding_data).identity("https://github.com/example/project/pull/7") == original
    for field, value in [
        ("review_id", 18),
        ("reviewer_id", 43),
        ("path", "other.py"),
        ("side", "LEFT"),
        ("suppressed_body", "Concern\ncode"),
    ]:
        updated = {**finding_data, field: value}
        assert Finding.model_validate(updated).identity("https://github.com/example/project/pull/7") != original
    assert finding.identity("https://github.com/example/project/pull/8") != original


def test_resources_include_supporting_tests_and_shared_effects(finding_data):
    finding_data["supporting_files"].append(r"SRC\Example.py")
    assert Finding.model_validate(finding_data).resources() == frozenset(
        {
            "file:src/example.py",
            "file:tests/test_example.py",
            "effect:branch-write",
        }
    )


@pytest.mark.parametrize(
    "updates",
    [
        {"comment_id": None},
        {"suppressed_body": "both"},
        {"comment_id": None, "suppressed_body": " \n"},
        {"review_id": True},
        {"reviewer_id": 0},
        {"comment_id": -1},
        {"side": "UNKNOWN"},
        {"path": "../x"},
        {"supporting_files": ["/tmp/x"]},
        {"side_effects": [""]},
        {"status": "accepted"},
        {"status": "reserved"},
        {"status": "acceptance_unknown"},
        {"status": "accepted", "attempt_id": "attempt"},
        {"status": "pending", "task_id": "task"},
        {"status": "pending", "attempt_id": "attempt"},
        {"status": "pending", "session_id": "session"},
        {"unrecognized": True},
    ],
)
def test_invalid_findings_fail_explicitly(finding_data, updates):
    with pytest.raises(ValidationError):
        Finding.model_validate({**finding_data, **updates})


@pytest.mark.parametrize("status", ["reserved", "acceptance_unknown", "accepted", "delivered", "resolved", "blocked"])
def test_lifecycle_records(finding_data, status):
    finding_data.update(status=status, attempt_id="attempt")
    if status in {"accepted", "delivered"}:
        finding_data["task_id"] = "task"
    assert Finding.model_validate(finding_data).status == status
