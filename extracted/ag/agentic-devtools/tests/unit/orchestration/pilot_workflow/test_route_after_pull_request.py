"""Tests for route_after_pull_request conditional edge function."""

from agentic_devtools.orchestration.pilot_workflow import route_after_pull_request


class TestRouteAfterPullRequest:
    def test_routes_to_completion_when_pr_created(self):
        assert route_after_pull_request({"pr_created": True}) == "completion"

    def test_routes_to_error_handler_when_error_present(self):
        assert route_after_pull_request({"error": "PR creation failed"}) == "error_handler"

    def test_routes_to_completion_legacy_fallback(self):
        """Legacy checkpoint fallback: absent pr_created routes to completion."""
        assert route_after_pull_request({}) == "completion"

    def test_routes_to_error_handler_when_pr_not_created(self):
        assert route_after_pull_request({"pr_created": False}) == "error_handler"

    def test_error_takes_precedence_over_pr_created(self):
        assert route_after_pull_request({"error": "boom", "pr_created": True}) == "error_handler"
