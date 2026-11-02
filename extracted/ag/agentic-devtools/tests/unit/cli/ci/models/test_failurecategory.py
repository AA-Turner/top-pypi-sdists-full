"""Tests for task inventory failure categories."""

from agentic_devtools.cli.ci.models import AgentTaskInventoryFailureCategory, FailureCategory


def test_canonical_enum_has_public_long_name() -> None:
    assert AgentTaskInventoryFailureCategory.__name__ == "AgentTaskInventoryFailureCategory"
    assert AgentTaskInventoryFailureCategory is FailureCategory


def test_failure_category_values() -> None:
    assert {item.value for item in FailureCategory} == {
        "http_not_found",
        "authentication",
        "permission",
        "malformed_response",
        "unknown_task_state",
        "retrieval_exhausted",
        "provider_unavailable",
    }
