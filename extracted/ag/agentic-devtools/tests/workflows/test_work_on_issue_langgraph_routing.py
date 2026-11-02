"""Compiled LangGraph workflow routing scenarios for work-on-issue."""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

from agentic_devtools.models.git_results import BlockedState, CommitResult, SetupResult
from agentic_devtools.orchestration.graph_builder import build_work_on_issue_graph

_STATE: dict[str, Any] = {
    "issue_key": "#42",
    "issue_provider": "github",
    "step": "",
    "status": "",
    "plan": "",
    "error": None,
    "retry_count": 0,
    "events": [],
}
_SETUP_RESULT = SetupResult(
    worktree_path="/tmp/issue-worktree",
    branch_name="feature/42/sibling-worktree",
    mode="created",
)


def _event(name: str) -> list[dict[str, str]]:
    return [{"event": name, "timestamp": "2024-01-01T00:00:00Z"}]


def _stub_initiate(_state):
    return {"step": "initiate", "status": "active", "error": None, "needs_setup": True, "events": _event("initiate")}


def _stub_setup(_state):
    return {"step": "setup", "error": None, "setup_result": _SETUP_RESULT, "events": _event("setup")}


def _stub_retrieve(_state):
    return {
        "step": "retrieve",
        "error": None,
        "issue_retrieved": True,
        "issue_data": {"summary": "Route PR from setup branch"},
        "events": _event("retrieve"),
    }


def _stub_planning(_state):
    return {"step": "planning", "error": None, "plan_posted": True, "plan": "Plan", "events": _event("planning")}


def _stub_checklist_creation(_state):
    return {"step": "checklist_creation", "error": None, "checklist_created": True, "events": _event("checklist")}


def _stub_implementation(_state):
    return {"step": "implementation", "error": None, "checklist_complete": True, "events": _event("implementation")}


def _stub_implementation_review(_state):
    return {
        "step": "implementation_review",
        "error": None,
        "verification_ready": True,
        "events": _event("implementation_review"),
    }


def _stub_verification(_state):
    return {"step": "verification", "error": None, "events": _event("verification")}


def _stub_completion(_state):
    return {"step": "completion", "status": "completed", "error": None, "events": _event("completion")}


class TestWorkOnIssueLanggraphRouting:
    def test_noop_commit_reaches_pr_with_branch_from_setup_result(self):
        captured: dict[str, str] = {}

        def stub_commit(_state):
            return {
                "step": "commit",
                "error": None,
                "commit_created": False,
                "commit_result": CommitResult(no_op=True, commit_message_title="feat(#42): test"),
                "events": _event("commit"),
            }

        def fake_create_pr(title: str, description: str, source_branch: str):
            captured["title"] = title
            captured["description"] = description
            captured["source_branch"] = source_branch
            return {"url": "https://github.com/swai-factory/agentic-devtools/pull/3632"}

        with (
            patch("agentic_devtools.orchestration.graph_builder.initiate_node", _stub_initiate),
            patch("agentic_devtools.orchestration.graph_builder.setup_node", _stub_setup),
            patch("agentic_devtools.orchestration.graph_builder.retrieve_node", _stub_retrieve),
            patch("agentic_devtools.orchestration.graph_builder.planning_node", _stub_planning),
            patch("agentic_devtools.orchestration.graph_builder.checklist_creation_node", _stub_checklist_creation),
            patch("agentic_devtools.orchestration.graph_builder.implementation_node", _stub_implementation),
            patch(
                "agentic_devtools.orchestration.graph_builder.implementation_review_node",
                _stub_implementation_review,
            ),
            patch("agentic_devtools.orchestration.graph_builder.verification_node", _stub_verification),
            patch("agentic_devtools.orchestration.graph_builder.commit_node", stub_commit),
            patch("agentic_devtools.orchestration.graph_builder.completion_node", _stub_completion),
            patch("agentic_devtools.orchestration.nodes.pull_request._create_github_pr", side_effect=fake_create_pr),
        ):
            compiled = build_work_on_issue_graph()
            result = compiled.invoke(dict(_STATE))

        assert result["step"] == "completion"
        assert result["status"] == "completed"
        assert captured["source_branch"] == "feature/42/sibling-worktree"
        assert captured["title"] == "feat(#42): test"

    def test_blocked_commit_routes_to_error_handler_before_pr(self):
        def stub_commit(_state):
            return {
                "step": "commit",
                "error": "push rejected",
                "commit_created": False,
                "commit_result": CommitResult(error=BlockedState(category="conflict", message="push rejected")),
                "events": _event("commit"),
            }

        def fail_if_called(_state):
            raise AssertionError("pull_request_node should not run when commit_result.error is set")

        with (
            patch("agentic_devtools.orchestration.graph_builder.initiate_node", _stub_initiate),
            patch("agentic_devtools.orchestration.graph_builder.setup_node", _stub_setup),
            patch("agentic_devtools.orchestration.graph_builder.retrieve_node", _stub_retrieve),
            patch("agentic_devtools.orchestration.graph_builder.planning_node", _stub_planning),
            patch("agentic_devtools.orchestration.graph_builder.checklist_creation_node", _stub_checklist_creation),
            patch("agentic_devtools.orchestration.graph_builder.implementation_node", _stub_implementation),
            patch(
                "agentic_devtools.orchestration.graph_builder.implementation_review_node",
                _stub_implementation_review,
            ),
            patch("agentic_devtools.orchestration.graph_builder.verification_node", _stub_verification),
            patch("agentic_devtools.orchestration.graph_builder.commit_node", stub_commit),
            patch("agentic_devtools.orchestration.graph_builder.pull_request_node", fail_if_called),
            patch("agentic_devtools.orchestration.graph_builder.completion_node", _stub_completion),
        ):
            compiled = build_work_on_issue_graph()
            result = compiled.invoke(dict(_STATE))

        assert result["step"] == "error_handler"
        assert result["status"] == "blocked"
        assert result["error"] == "push rejected"
        assert result["commit_created"] is False
        assert result["commit_result"].error is not None
        assert result["commit_result"].error.category == "conflict"
