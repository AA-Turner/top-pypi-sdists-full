"""Tests for route_after_implementation conditional edge function."""

from agentic_devtools.orchestration.pilot_workflow import route_after_implementation


class TestRouteAfterImplementation:
    def test_routes_to_implementation_review_when_checklist_complete(self):
        assert route_after_implementation({"checklist_complete": True}) == "implementation_review"

    def test_routes_to_implementation_review_legacy_fallback(self):
        """Legacy checkpoint fallback: absent signal routes to implementation_review."""
        assert route_after_implementation({}) == "implementation_review"

    def test_routes_to_error_handler_when_error_present(self):
        assert route_after_implementation({"error": "something"}) == "error_handler"

    def test_routes_to_error_handler_when_checklist_not_complete(self):
        assert route_after_implementation({"checklist_complete": False}) == "error_handler"

    def test_error_takes_precedence_over_checklist_complete(self):
        assert route_after_implementation({"error": "boom", "checklist_complete": True}) == "error_handler"
