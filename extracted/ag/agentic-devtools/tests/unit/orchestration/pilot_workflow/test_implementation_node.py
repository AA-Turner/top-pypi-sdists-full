"""Tests for implementation_node stub function."""

from agentic_devtools.orchestration.pilot_workflow import implementation_node


class TestImplementationNode:
    def test_returns_step_implementation(self):
        result = implementation_node({})
        assert result["step"] == "implementation"

    def test_appends_event(self):
        result = implementation_node({})
        assert len(result["events"]) == 1
        assert result["events"][0]["event"] == "implementation_completed"

    def test_event_has_timestamp(self):
        result = implementation_node({})
        assert "timestamp" in result["events"][0]

    def test_clears_error_from_verification_retry(self):
        """Clearing error lets route_after_implementation proceed to implementation_review."""
        result = implementation_node({"error": "tests failed"})
        assert result["error"] is None
