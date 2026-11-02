"""Tests for route_after_plan conditional edge function."""

from agentic_devtools.orchestration.pilot_workflow import route_after_plan


class TestRouteAfterPlan:
    def test_routes_to_checklist_creation_when_no_error(self):
        assert route_after_plan({"plan": "the plan", "plan_posted": True}) == "checklist_creation"

    def test_routes_to_checklist_creation_when_key_missing(self):
        """A missing plan_posted flag must not halt the workflow."""
        assert route_after_plan({}) == "checklist_creation"

    def test_best_effort_post_failure_still_advances(self):
        """plan_posted False (dry-run or failed post) is best-effort and still advances."""
        assert route_after_plan({"plan": "the plan", "plan_posted": False}) == "checklist_creation"

    def test_routes_to_error_handler_when_error_present(self):
        assert route_after_plan({"error": "planning failed"}) == "error_handler"

    def test_error_takes_precedence_over_plan(self):
        assert route_after_plan({"error": "boom", "plan_posted": True}) == "error_handler"
