"""Tests for route_after_checklist_creation conditional edge function."""

from agentic_devtools.orchestration.pilot_workflow import route_after_checklist_creation


class TestRouteAfterChecklistCreation:
    def test_routes_to_error_handler_when_error_present(self):
        assert route_after_checklist_creation({"error": "creation failed"}) == "error_handler"

    def test_routes_to_implementation_when_checklist_created(self):
        assert route_after_checklist_creation({"checklist_created": True}) == "implementation"

    def test_routes_to_implementation_when_legacy_state_has_no_signal(self):
        assert route_after_checklist_creation({}) == "implementation"

    def test_routes_to_error_handler_when_checklist_created_false(self):
        assert route_after_checklist_creation({"checklist_created": False}) == "error_handler"
