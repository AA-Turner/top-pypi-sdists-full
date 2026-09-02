"""Tests for route_after_implementation_review conditional edge function."""

from agentic_devtools.orchestration.pilot_workflow import route_after_implementation_review


class TestRouteAfterImplementationReview:
    def test_routes_to_verification_when_ready(self):
        assert route_after_implementation_review({"verification_ready": True}) == "verification"

    def test_routes_to_error_handler_when_error_present(self):
        assert route_after_implementation_review({"error": "review failed"}) == "error_handler"

    def test_routes_to_verification_legacy_fallback(self):
        """Legacy checkpoint fallback: absent signal routes to verification."""
        assert route_after_implementation_review({}) == "verification"

    def test_routes_to_error_handler_when_not_ready(self):
        assert route_after_implementation_review({"verification_ready": False}) == "error_handler"

    def test_error_takes_precedence_over_verification_ready(self):
        assert route_after_implementation_review({"error": "boom", "verification_ready": True}) == "error_handler"
