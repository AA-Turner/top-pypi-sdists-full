"""Tests for route_after_initiate conditional edge function."""

from agentic_devtools.orchestration.pilot_workflow import route_after_initiate


class TestRouteAfterInitiate:
    def test_routes_to_error_handler_when_error_present(self):
        assert route_after_initiate({"error": "pre-flight failed"}) == "error_handler"

    def test_routes_to_setup_when_needs_setup(self):
        assert route_after_initiate({"needs_setup": True}) == "setup"

    def test_routes_to_setup_when_no_error_and_no_setup(self):
        """Pre-flight OK (no error, needs_setup absent) → setup; issue_retrieved is ignored."""
        assert route_after_initiate({"issue_retrieved": True}) == "setup"

    def test_routes_to_setup_when_no_signals_legacy_fallback(self):
        """Legacy checkpoint fallback: absent signal fields route to setup."""
        assert route_after_initiate({}) == "setup"

    def test_routes_to_setup_when_error_is_none(self):
        assert route_after_initiate({"error": None, "issue_retrieved": True}) == "setup"

    def test_routes_to_setup_when_error_is_empty_string(self):
        assert route_after_initiate({"error": "", "issue_retrieved": True}) == "setup"

    def test_error_takes_precedence_over_issue_retrieved(self):
        assert route_after_initiate({"error": "boom", "issue_retrieved": True}) == "error_handler"

    def test_error_takes_precedence_over_needs_setup(self):
        assert route_after_initiate({"error": "boom", "needs_setup": True}) == "error_handler"

    def test_needs_setup_takes_precedence_over_issue_retrieved(self):
        assert route_after_initiate({"needs_setup": True, "issue_retrieved": True}) == "setup"

    def test_routes_to_setup_when_needs_setup_false_and_issue_retrieved_false(self):
        """needs_setup explicitly False and no error → setup; issue_retrieved is not consulted."""
        assert route_after_initiate({"issue_retrieved": False, "needs_setup": False}) == "setup"
