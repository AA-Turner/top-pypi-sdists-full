"""Tests for build_work_on_issue_graph factory function."""

import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.state import CompiledStateGraph

from agentic_devtools.orchestration.graph_builder import build_work_on_issue_graph


class TestBuildWorkOnIssueGraph:
    """Tests for build_work_on_issue_graph()."""

    def test_returns_compiled_state_graph(self):
        compiled = build_work_on_issue_graph()
        assert isinstance(compiled, CompiledStateGraph)

    def test_graph_contains_all_expected_nodes(self):
        compiled = build_work_on_issue_graph()
        node_names = set(compiled.get_graph().nodes.keys())
        expected = {
            "__start__",
            "__end__",
            "initiate",
            "setup",
            "retrieve",
            "planning",
            "checklist_creation",
            "implementation",
            "implementation_review",
            "verification",
            "commit",
            "pull_request",
            "completion",
            "error_handler",
        }
        assert expected == node_names

    def test_graph_does_not_contain_planning_gate(self):
        compiled = build_work_on_issue_graph()
        node_names = set(compiled.get_graph().nodes.keys())
        assert "planning_gate" not in node_names

    def test_compiles_without_checkpointer(self):
        compiled = build_work_on_issue_graph(checkpointer=None)
        assert compiled is not None

    def test_compiles_with_checkpointer(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        conn = sqlite3.connect(db_path, check_same_thread=False)
        saver = SqliteSaver(conn)
        saver.setup()
        try:
            compiled = build_work_on_issue_graph(checkpointer=saver)
            assert isinstance(compiled, CompiledStateGraph)
        finally:
            conn.close()

    def test_happy_path_execution_reaches_completion(self):
        compiled = build_work_on_issue_graph()
        # Patch node implementations with stubs for integration testing
        from unittest.mock import patch

        from agentic_devtools.orchestration.pilot_workflow import (
            checklist_creation_node as stub_checklist,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            commit_node as stub_commit,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            completion_node as stub_completion,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            implementation_node as stub_impl,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            implementation_review_node as stub_review,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            planning_node as stub_planning,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            pull_request_node as stub_pr,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            setup_node as stub_setup,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            verification_node as stub_verify,
        )

        # Stub initiate and retrieve for tests
        def stub_initiate(state):
            return {
                "step": "initiate",
                "status": "active",
                "error": None,
                "issue_provider": "jira",
                "issue_retrieved": True,
                "needs_setup": False,
                "events": [{"event": "initiate_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_retrieve(state):
            return {
                "step": "retrieve",
                "error": None,
                "issue_data": {"key": "TEST-1", "summary": "test"},
                "issue_retrieved": True,
                "events": [{"event": "retrieve_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        with (
            patch("agentic_devtools.orchestration.graph_builder.initiate_node", stub_initiate),
            patch("agentic_devtools.orchestration.graph_builder.retrieve_node", stub_retrieve),
            patch("agentic_devtools.orchestration.graph_builder.setup_node", stub_setup),
            patch("agentic_devtools.orchestration.graph_builder.planning_node", stub_planning),
            patch("agentic_devtools.orchestration.graph_builder.checklist_creation_node", stub_checklist),
            patch("agentic_devtools.orchestration.graph_builder.implementation_node", stub_impl),
            patch("agentic_devtools.orchestration.graph_builder.implementation_review_node", stub_review),
            patch("agentic_devtools.orchestration.graph_builder.verification_node", stub_verify),
            patch("agentic_devtools.orchestration.graph_builder.commit_node", stub_commit),
            patch("agentic_devtools.orchestration.graph_builder.pull_request_node", stub_pr),
            patch("agentic_devtools.orchestration.graph_builder.completion_node", stub_completion),
        ):
            compiled = build_work_on_issue_graph()
            result = compiled.invoke(
                {
                    "issue_key": "TEST-1",
                    "step": "",
                    "status": "",
                    "plan": "",
                    "error": None,
                    "retry_count": 0,
                    "events": [],
                }
            )
            assert result["step"] == "completion"
            assert result["status"] == "completed"

    def test_happy_path_accumulates_events(self):
        from unittest.mock import patch

        from agentic_devtools.orchestration.pilot_workflow import (
            checklist_creation_node as stub_checklist,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            commit_node as stub_commit,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            completion_node as stub_completion,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            implementation_node as stub_impl,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            implementation_review_node as stub_review,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            planning_node as stub_planning,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            pull_request_node as stub_pr,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            setup_node as stub_setup,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            verification_node as stub_verify,
        )

        def stub_initiate(state):
            return {
                "step": "initiate",
                "status": "active",
                "error": None,
                "issue_provider": "jira",
                "issue_retrieved": True,
                "needs_setup": False,
                "events": [{"event": "initiate_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_retrieve(state):
            return {
                "step": "retrieve",
                "error": None,
                "issue_data": {"key": "TEST-1", "summary": "test"},
                "issue_retrieved": True,
                "events": [{"event": "retrieve_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        with (
            patch("agentic_devtools.orchestration.graph_builder.initiate_node", stub_initiate),
            patch("agentic_devtools.orchestration.graph_builder.retrieve_node", stub_retrieve),
            patch("agentic_devtools.orchestration.graph_builder.setup_node", stub_setup),
            patch("agentic_devtools.orchestration.graph_builder.planning_node", stub_planning),
            patch("agentic_devtools.orchestration.graph_builder.checklist_creation_node", stub_checklist),
            patch("agentic_devtools.orchestration.graph_builder.implementation_node", stub_impl),
            patch("agentic_devtools.orchestration.graph_builder.implementation_review_node", stub_review),
            patch("agentic_devtools.orchestration.graph_builder.verification_node", stub_verify),
            patch("agentic_devtools.orchestration.graph_builder.commit_node", stub_commit),
            patch("agentic_devtools.orchestration.graph_builder.pull_request_node", stub_pr),
            patch("agentic_devtools.orchestration.graph_builder.completion_node", stub_completion),
        ):
            compiled = build_work_on_issue_graph()
            result = compiled.invoke(
                {
                    "issue_key": "TEST-1",
                    "step": "",
                    "status": "",
                    "plan": "",
                    "error": None,
                    "retry_count": 0,
                    "events": [],
                }
            )
            event_names = [e["event"] for e in result["events"]]
            assert "initiate_completed" in event_names
            assert "planning_completed" in event_names
            assert "completion_completed" in event_names

    def test_error_path_routes_through_setup(self):
        from unittest.mock import patch

        from agentic_devtools.orchestration.pilot_workflow import (
            checklist_creation_node as stub_checklist,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            commit_node as stub_commit,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            completion_node as stub_completion,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            implementation_node as stub_impl,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            implementation_review_node as stub_review,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            planning_node as stub_planning,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            pull_request_node as stub_pr,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            setup_node as stub_setup,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            verification_node as stub_verify,
        )

        def stub_initiate(state):
            pre_flight_error = state.get("error")
            needs_setup = bool(pre_flight_error)
            issue_retrieved = not needs_setup
            return {
                "step": "initiate",
                "status": "active",
                "error": None,
                "issue_provider": "jira",
                "issue_retrieved": issue_retrieved,
                "needs_setup": needs_setup,
                "events": [{"event": "initiate_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_retrieve(state):
            return {
                "step": "retrieve",
                "error": None,
                "issue_data": {"key": "TEST-1", "summary": "test"},
                "issue_retrieved": True,
                "events": [{"event": "retrieve_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        with (
            patch("agentic_devtools.orchestration.graph_builder.initiate_node", stub_initiate),
            patch("agentic_devtools.orchestration.graph_builder.retrieve_node", stub_retrieve),
            patch("agentic_devtools.orchestration.graph_builder.setup_node", stub_setup),
            patch("agentic_devtools.orchestration.graph_builder.planning_node", stub_planning),
            patch("agentic_devtools.orchestration.graph_builder.checklist_creation_node", stub_checklist),
            patch("agentic_devtools.orchestration.graph_builder.implementation_node", stub_impl),
            patch("agentic_devtools.orchestration.graph_builder.implementation_review_node", stub_review),
            patch("agentic_devtools.orchestration.graph_builder.verification_node", stub_verify),
            patch("agentic_devtools.orchestration.graph_builder.commit_node", stub_commit),
            patch("agentic_devtools.orchestration.graph_builder.pull_request_node", stub_pr),
            patch("agentic_devtools.orchestration.graph_builder.completion_node", stub_completion),
        ):
            compiled = build_work_on_issue_graph()
            result = compiled.invoke(
                {
                    "issue_key": "TEST-1",
                    "step": "",
                    "status": "",
                    "plan": "",
                    "error": "pre-flight failed",
                    "retry_count": 0,
                    "events": [],
                }
            )
            event_names = [e["event"] for e in result["events"]]
            assert "setup_completed" in event_names
            assert result["step"] == "completion"

    def test_error_handler_terminates_graph(self):
        """Graph routes to error_handler when planning has an explicit error."""
        from unittest.mock import patch

        from agentic_devtools.orchestration.pilot_workflow import (
            checklist_creation_node as stub_checklist,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            commit_node as stub_commit,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            completion_node as stub_completion,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            implementation_node as stub_impl,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            implementation_review_node as stub_review,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            pull_request_node as stub_pr,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            setup_node as stub_setup,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            verification_node as stub_verify,
        )

        def stub_initiate(state):
            return {
                "step": "initiate",
                "status": "active",
                "error": None,
                "issue_provider": "jira",
                "issue_retrieved": True,
                "needs_setup": False,
                "events": [{"event": "initiate_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_retrieve(state):
            return {
                "step": "retrieve",
                "error": None,
                "issue_data": {"key": "TEST-1", "summary": "test"},
                "issue_retrieved": True,
                "events": [{"event": "retrieve_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def failing_planning_node(state):
            return {
                "step": "planning",
                "error": "planning exploded",
                "plan_posted": False,
                "events": [{"event": "planning_failed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        with (
            patch("agentic_devtools.orchestration.graph_builder.initiate_node", stub_initiate),
            patch("agentic_devtools.orchestration.graph_builder.retrieve_node", stub_retrieve),
            patch("agentic_devtools.orchestration.graph_builder.setup_node", stub_setup),
            patch("agentic_devtools.orchestration.graph_builder.planning_node", failing_planning_node),
            patch("agentic_devtools.orchestration.graph_builder.checklist_creation_node", stub_checklist),
            patch("agentic_devtools.orchestration.graph_builder.implementation_node", stub_impl),
            patch("agentic_devtools.orchestration.graph_builder.implementation_review_node", stub_review),
            patch("agentic_devtools.orchestration.graph_builder.verification_node", stub_verify),
            patch("agentic_devtools.orchestration.graph_builder.commit_node", stub_commit),
            patch("agentic_devtools.orchestration.graph_builder.pull_request_node", stub_pr),
            patch("agentic_devtools.orchestration.graph_builder.completion_node", stub_completion),
        ):
            compiled = build_work_on_issue_graph()
            result = compiled.invoke(
                {
                    "issue_key": "TEST-1",
                    "step": "",
                    "status": "",
                    "plan": "",
                    "error": None,
                    "retry_count": 0,
                    "events": [],
                }
            )
            assert result["status"] == "failed"
            assert result["step"] == "error_handler"

    def test_happy_path_traversal_reaches_completion(self):
        """SC-004: Full graph traversal initiate→completion with stub nodes."""
        from unittest.mock import patch

        from agentic_devtools.orchestration.pilot_workflow import (
            checklist_creation_node as stub_checklist,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            commit_node as stub_commit,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            completion_node as stub_completion,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            implementation_node as stub_impl,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            implementation_review_node as stub_review,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            planning_node as stub_planning,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            pull_request_node as stub_pr,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            setup_node as stub_setup,
        )
        from agentic_devtools.orchestration.pilot_workflow import (
            verification_node as stub_verify,
        )

        def stub_initiate(state):
            return {
                "step": "initiate",
                "status": "active",
                "error": None,
                "issue_provider": "jira",
                "issue_retrieved": True,
                "needs_setup": False,
                "events": [{"event": "initiate_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_retrieve(state):
            return {
                "step": "retrieve",
                "error": None,
                "issue_data": {"key": "PERF-1", "summary": "test"},
                "issue_retrieved": True,
                "events": [{"event": "retrieve_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        with (
            patch("agentic_devtools.orchestration.graph_builder.initiate_node", stub_initiate),
            patch("agentic_devtools.orchestration.graph_builder.retrieve_node", stub_retrieve),
            patch("agentic_devtools.orchestration.graph_builder.setup_node", stub_setup),
            patch("agentic_devtools.orchestration.graph_builder.planning_node", stub_planning),
            patch("agentic_devtools.orchestration.graph_builder.checklist_creation_node", stub_checklist),
            patch("agentic_devtools.orchestration.graph_builder.implementation_node", stub_impl),
            patch("agentic_devtools.orchestration.graph_builder.implementation_review_node", stub_review),
            patch("agentic_devtools.orchestration.graph_builder.verification_node", stub_verify),
            patch("agentic_devtools.orchestration.graph_builder.commit_node", stub_commit),
            patch("agentic_devtools.orchestration.graph_builder.pull_request_node", stub_pr),
            patch("agentic_devtools.orchestration.graph_builder.completion_node", stub_completion),
        ):
            compiled = build_work_on_issue_graph()
            result = compiled.invoke(
                {
                    "issue_key": "PERF-1",
                    "step": "",
                    "status": "",
                    "plan": "",
                    "error": None,
                    "retry_count": 0,
                    "events": [],
                }
            )
            assert result["step"] == "completion"

    def test_entry_point_is_initiate(self):
        compiled = build_work_on_issue_graph()
        graph = compiled.get_graph()
        start_edges = [e for e in graph.edges if e.source == "__start__"]
        assert len(start_edges) == 1
        assert start_edges[0].target == "initiate"

    def test_compiled_graph_preserves_planning_dry_run_flag(self):
        from unittest.mock import patch

        def stub_initiate(state):
            return {
                "step": "initiate",
                "status": "active",
                "error": None,
                "issue_provider": "jira",
                "issue_retrieved": True,
                "needs_setup": False,
                "events": [{"event": "initiate_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_retrieve(state):
            return {
                "step": "retrieve",
                "error": None,
                "issue_data": {"key": "TEST-1", "summary": "test"},
                "issue_retrieved": True,
                "events": [{"event": "retrieve_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_setup(state):
            return {
                "step": "setup",
                "error": None,
                "setup_complete": True,
                "events": [{"event": "setup_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_planning(state):
            return {
                "step": "planning",
                "status": "active",
                "error": None,
                "plan": "plan",
                "plan_posted": True,
                "dry_run_skipped": True,
                "events": [{"event": "planning_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_checklist(state):
            return {"step": "checklist_creation", "checklist_created": False, "error": "stop"}

        def stub_error_handler(state):
            return {"step": "error_handler", "status": "failed", "error": state.get("error"), "events": []}

        with (
            patch("agentic_devtools.orchestration.graph_builder.initiate_node", stub_initiate),
            patch("agentic_devtools.orchestration.graph_builder.setup_node", stub_setup),
            patch("agentic_devtools.orchestration.graph_builder.retrieve_node", stub_retrieve),
            patch("agentic_devtools.orchestration.graph_builder.planning_node", stub_planning),
            patch("agentic_devtools.orchestration.graph_builder.checklist_creation_node", stub_checklist),
            patch("agentic_devtools.orchestration.graph_builder.error_handler_node", stub_error_handler),
        ):
            compiled = build_work_on_issue_graph()
            result = compiled.invoke({"issue_key": "TEST-1", "events": [], "retry_count": 0})

        assert result["dry_run_skipped"] is True

    def test_compiled_graph_preserves_completion_comment_post_result(self):
        from unittest.mock import patch

        def stub_initiate(state):
            return {
                "step": "initiate",
                "status": "active",
                "error": None,
                "issue_provider": "jira",
                "issue_retrieved": True,
                "needs_setup": False,
                "events": [{"event": "initiate_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_retrieve(state):
            return {
                "step": "retrieve",
                "error": None,
                "issue_data": {"key": "TEST-1", "summary": "test"},
                "issue_retrieved": True,
                "events": [{"event": "retrieve_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_setup(state):
            return {
                "step": "setup",
                "error": None,
                "setup_complete": True,
                "events": [{"event": "setup_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_planning(state):
            return {
                "step": "planning",
                "status": "active",
                "error": None,
                "plan": "plan",
                "plan_posted": True,
                "events": [{"event": "planning_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_checklist(state):
            return {
                "step": "checklist_creation",
                "checklist_created": True,
                "events": [{"event": "checklist_creation_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_impl(state):
            return {
                "step": "implementation",
                "error": None,
                "checklist_complete": True,
                "events": [{"event": "implementation_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_review(state):
            return {
                "step": "implementation_review",
                "verification_ready": True,
                "events": [{"event": "implementation_review_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_verify(state):
            return {
                "step": "verification",
                "error": None,
                "retry_count": 0,
                "events": [{"event": "verification_passed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_commit(state):
            return {
                "step": "commit",
                "commit_created": True,
                "branch_pushed": True,
                "events": [{"event": "commit_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_pr(state):
            return {
                "step": "pull_request",
                "pr_created": True,
                "events": [{"event": "pull_request_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        def stub_completion(state):
            return {
                "step": "completion",
                "status": "completed",
                "completion_comment_posted": True,
                "dry_run_skipped": False,
                "events": [{"event": "completion_completed", "timestamp": "2024-01-01T00:00:00Z"}],
            }

        with (
            patch("agentic_devtools.orchestration.graph_builder.initiate_node", stub_initiate),
            patch("agentic_devtools.orchestration.graph_builder.setup_node", stub_setup),
            patch("agentic_devtools.orchestration.graph_builder.retrieve_node", stub_retrieve),
            patch("agentic_devtools.orchestration.graph_builder.planning_node", stub_planning),
            patch("agentic_devtools.orchestration.graph_builder.checklist_creation_node", stub_checklist),
            patch("agentic_devtools.orchestration.graph_builder.implementation_node", stub_impl),
            patch("agentic_devtools.orchestration.graph_builder.implementation_review_node", stub_review),
            patch("agentic_devtools.orchestration.graph_builder.verification_node", stub_verify),
            patch("agentic_devtools.orchestration.graph_builder.commit_node", stub_commit),
            patch("agentic_devtools.orchestration.graph_builder.pull_request_node", stub_pr),
            patch("agentic_devtools.orchestration.graph_builder.completion_node", stub_completion),
        ):
            compiled = build_work_on_issue_graph()
            result = compiled.invoke({"issue_key": "TEST-1", "events": [], "retry_count": 0})

        assert result["completion_comment_posted"] is True

    def test_completion_connects_to_end(self):
        compiled = build_work_on_issue_graph()
        graph = compiled.get_graph()
        completion_edges = [e for e in graph.edges if e.source == "completion"]
        targets = {e.target for e in completion_edges}
        assert "__end__" in targets

    def test_error_handler_connects_to_end(self):
        compiled = build_work_on_issue_graph()
        graph = compiled.get_graph()
        error_edges = [e for e in graph.edges if e.source == "error_handler"]
        targets = {e.target for e in error_edges}
        assert "__end__" in targets

    def test_setup_can_route_to_error_handler(self):
        compiled = build_work_on_issue_graph()
        graph = compiled.get_graph()
        setup_edges = [e for e in graph.edges if e.source == "setup"]
        targets = {e.target for e in setup_edges}
        assert "retrieve" in targets
        assert "error_handler" in targets

    def test_checklist_creation_can_route_to_error_handler(self):
        compiled = build_work_on_issue_graph()
        graph = compiled.get_graph()
        checklist_edges = [e for e in graph.edges if e.source == "checklist_creation"]
        targets = {e.target for e in checklist_edges}
        assert "implementation" in targets
        assert "error_handler" in targets

    def test_initiate_routes_to_setup_and_error_handler_only(self):
        """route_after_initiate only returns 'setup' or 'error_handler'; 'retrieve' must not appear."""
        compiled = build_work_on_issue_graph()
        graph = compiled.get_graph()
        initiate_edges = [e for e in graph.edges if e.source == "initiate"]
        targets = {e.target for e in initiate_edges}
        assert "setup" in targets
        assert "error_handler" in targets
        assert "retrieve" not in targets
