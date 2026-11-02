"""Tests for the canonical public inventory failure category."""

from agentic_devtools.cli.ci.models import AgentTaskInventoryFailureCategory


def test_not_found_is_a_fact_not_capability_classification() -> None:
    assert AgentTaskInventoryFailureCategory.HTTP_NOT_FOUND.value == "http_not_found"
