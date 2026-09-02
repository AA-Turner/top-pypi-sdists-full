"""Tests for WorkOnIssueState TypedDict schema."""

import operator
from typing import Annotated, get_args, get_origin, get_type_hints

from agentic_devtools.orchestration.state_schema import WorkOnIssueEvent, WorkOnIssueState


class TestWorkOnIssueState:
    """Tests for WorkOnIssueState TypedDict."""

    def test_can_instantiate_with_all_fields(self):
        state: WorkOnIssueState = {
            "issue_key": "TEST-123",
            "step": "initiate",
            "status": "active",
            "plan": "",
            "error": None,
            "retry_count": 0,
            "events": [],
        }
        assert state["issue_key"] == "TEST-123"
        assert state["step"] == "initiate"
        assert state["status"] == "active"
        assert state["plan"] == ""
        assert state["error"] is None
        assert state["retry_count"] == 0
        assert state["events"] == []

    def test_total_false_allows_partial_instantiation(self):
        state: WorkOnIssueState = {"issue_key": "TEST-456"}  # type: ignore[typeddict-item, annotation-unchecked]
        assert state["issue_key"] == "TEST-456"

    def test_events_field_has_add_reducer_annotation(self):
        hints = get_type_hints(WorkOnIssueState, include_extras=True)
        events_hint = hints["events"]
        assert hasattr(events_hint, "__metadata__")
        assert events_hint.__metadata__[0] is operator.add

    def test_events_reducer_appends_with_operator_add(self):
        existing: list[WorkOnIssueEvent] = [{"event": "a", "timestamp": "t1"}]
        new: list[WorkOnIssueEvent] = [{"event": "b", "timestamp": "t2"}]
        result = operator.add(existing, new)
        assert result == [{"event": "a", "timestamp": "t1"}, {"event": "b", "timestamp": "t2"}]

    def test_events_reducer_works_with_empty_initial(self):
        result = operator.add([], [{"event": "first", "timestamp": "t1"}])
        assert result == [{"event": "first", "timestamp": "t1"}]

    def test_schema_fields_include_expected_keys(self):
        hints = get_type_hints(WorkOnIssueState, include_extras=True)
        expected = {
            "issue_key",
            "step",
            "status",
            "plan",
            "error",
            "retry_count",
            "events",
            "agent_context",
            "affected_paths",
            # Routing signal fields
            "issue_retrieved",
            "needs_setup",
            "plan_posted",
            "checklist_complete",
            "verification_ready",
            "commit_created",
            "branch_pushed",
            "pr_created",
            # Additional checkpoint-compatibility routing fields
            "setup_complete",
            "checklist_created",
            "dry_run",
            "dry_run_skipped",
            "completion_comment_posted",
            # Node status tracking for checkpoint/resume (FR-002, FR-010)
            "_node_statuses",
            # Workflow run identifier — persisted in graph state for checkpoint/resume
            "run_id",
            # Autonomous workflow fields (issue #1897)
            "issue_provider",
            "issue_data",
            "checklist_items",
            "implementation_log",
            "verification_output",
            "pr_url",
            "commit_message",
            "pr_title",
            "retry_budget",
            "token_usage_prompt",
            "token_usage_completion",
            "blocked_reason",
            # Worktree setup / git ops nodes (issue #1900)
            "setup_result",
            "commit_result",
            "source_branch",
            "skip_rebase",
        }
        assert expected == set(hints.keys())

    def test_error_field_accepts_none(self):
        state: WorkOnIssueState = {
            "issue_key": "X",
            "step": "",
            "status": "",
            "plan": "",
            "error": None,
            "retry_count": 0,
            "events": [],
        }
        assert state["error"] is None

    def test_error_field_accepts_string(self):
        state: WorkOnIssueState = {
            "issue_key": "X",
            "step": "",
            "status": "",
            "plan": "",
            "error": "something went wrong",
            "retry_count": 0,
            "events": [],
        }
        assert state["error"] == "something went wrong"

    def test_events_field_is_typed_with_workonissueevent(self):
        hints = get_type_hints(WorkOnIssueState, include_extras=True)
        events_hint = hints["events"]
        # Annotated[list[WorkOnIssueEvent], operator.add] — verify the underlying type
        assert get_origin(events_hint) is Annotated
        underlying_type, *metadata = get_args(events_hint)
        assert underlying_type == list[WorkOnIssueEvent]
        assert operator.add in metadata
