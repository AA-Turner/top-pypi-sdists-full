"""Tests for planning_node blocked detection."""

from agentic_devtools.orchestration.nodes.planning import _check_blocked


class TestCheckBlocked:
    def test_empty_summary_is_blocked(self):
        result = _check_blocked("", "Some description")
        assert result is not None
        assert "summary" in result.lower()

    def test_short_summary_is_blocked(self):
        result = _check_blocked("hi", "Some description here that is long enough")
        assert result is not None

    def test_empty_description_is_blocked(self):
        result = _check_blocked("Valid summary here", "")
        assert result is not None
        assert "description" in result.lower()

    def test_short_description_is_blocked(self):
        result = _check_blocked("Valid summary here", "short")
        assert result is not None

    def test_valid_issue_is_not_blocked(self):
        result = _check_blocked(
            "Add user authentication endpoint",
            "Implement a REST endpoint for user login with JWT tokens and proper error handling",
        )
        assert result is None
