"""Tests for route_after_retrieve in pilot_workflow."""

from agentic_devtools.orchestration.pilot_workflow import route_after_retrieve


class TestRouteAfterRetrieve:
    def test_routes_to_error_handler_when_error_present(self):
        assert route_after_retrieve({"error": "retrieval failed"}) == "error_handler"

    def test_routes_to_planning_when_issue_retrieved(self):
        assert route_after_retrieve({"issue_retrieved": True}) == "planning"

    def test_routes_to_planning_when_key_absent(self):
        assert route_after_retrieve({}) == "planning"

    def test_routes_to_error_handler_when_issue_retrieved_false(self):
        assert route_after_retrieve({"issue_retrieved": False}) == "error_handler"
