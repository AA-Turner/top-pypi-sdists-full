"""Tests verifying routing functions handle minimal/legacy state without KeyError.

These tests simulate checkpoint compatibility: a state dict that was persisted
*before* the routing-signal fields were introduced (i.e., only contains `issue_key`)
should still pass through every routing function without raising exceptions.
"""

from typing import Any, cast

import pytest

from agentic_devtools.orchestration.pilot_workflow import (
    route_after_checklist_creation,
    route_after_commit,
    route_after_implementation,
    route_after_implementation_review,
    route_after_initiate,
    route_after_plan,
    route_after_pull_request,
    route_after_retrieve,
    route_after_setup,
    route_after_verify,
)
from agentic_devtools.orchestration.state_schema import WorkOnIssueState


@pytest.fixture
def minimal_state() -> WorkOnIssueState:
    """State dict with only issue_key — simulates a legacy checkpoint."""
    return cast(WorkOnIssueState, {"issue_key": "TEST-1"})


class TestCheckpointCompatibility:
    """Every routing function must handle minimal state gracefully (no KeyError)."""

    def test_route_after_initiate_minimal(self, minimal_state: WorkOnIssueState) -> None:
        result = route_after_initiate(minimal_state)
        # Legacy fallback: no signal fields → returns "retrieve" (post-refactor default)
        assert result in ("setup", "retrieve", "error_handler")

    def test_route_after_plan_minimal(self, minimal_state: WorkOnIssueState) -> None:
        result = route_after_plan(minimal_state)
        assert result in ("checklist_creation", "error_handler")

    def test_route_after_setup_minimal(self, minimal_state: WorkOnIssueState) -> None:
        result = route_after_setup(minimal_state)
        assert result in ("retrieve", "error_handler")

    def test_route_after_retrieve_minimal(self, minimal_state: WorkOnIssueState) -> None:
        result = route_after_retrieve(minimal_state)
        assert result in ("planning", "error_handler")

    def test_route_after_checklist_creation_minimal(self, minimal_state: WorkOnIssueState) -> None:
        result = route_after_checklist_creation(minimal_state)
        assert result in ("implementation", "error_handler")

    def test_route_after_implementation_minimal(self, minimal_state: WorkOnIssueState) -> None:
        result = route_after_implementation(minimal_state)
        assert result in ("implementation_review", "error_handler")

    def test_route_after_implementation_review_minimal(self, minimal_state: WorkOnIssueState) -> None:
        result = route_after_implementation_review(minimal_state)
        assert result in ("verification", "error_handler")

    def test_route_after_verify_minimal(self, minimal_state: WorkOnIssueState) -> None:
        result = route_after_verify(minimal_state)
        assert result in ("implementation", "commit", "error_handler")

    def test_route_after_commit_minimal(self, minimal_state: WorkOnIssueState) -> None:
        result = route_after_commit(minimal_state)
        assert result in ("pull_request", "error_handler")

    def test_route_after_pull_request_minimal(self, minimal_state: WorkOnIssueState) -> None:
        result = route_after_pull_request(minimal_state)
        assert result in ("completion", "error_handler")

    def test_no_keyerror_with_empty_state(self) -> None:
        """Even a completely empty state must not raise KeyError."""
        empty = cast(WorkOnIssueState, {})
        fns: list[Any] = [
            route_after_initiate,
            route_after_setup,
            route_after_retrieve,
            route_after_plan,
            route_after_checklist_creation,
            route_after_implementation,
            route_after_implementation_review,
            route_after_verify,
            route_after_commit,
            route_after_pull_request,
        ]
        for fn in fns:
            # Should not raise
            result = fn(empty)
            assert isinstance(result, str)
