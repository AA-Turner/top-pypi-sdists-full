"""Tests for route_after_verify conditional edge function."""

from agentic_devtools.orchestration.pilot_workflow import MAX_RETRIES, route_after_verify


class TestRouteAfterVerify:
    def test_routes_to_commit_when_no_error(self):
        assert route_after_verify({"error": None, "retry_count": 0}) == "commit"

    def test_routes_to_commit_when_error_missing(self):
        assert route_after_verify({}) == "commit"

    def test_routes_to_implementation_on_retryable_error(self):
        assert route_after_verify({"error": "test failed", "retry_count": 0}) == "implementation"

    def test_routes_to_implementation_below_max_retries(self):
        assert route_after_verify({"error": "test failed", "retry_count": MAX_RETRIES - 1}) == "implementation"

    def test_routes_to_error_handler_at_max_retries(self):
        assert route_after_verify({"error": "test failed", "retry_count": MAX_RETRIES}) == "error_handler"

    def test_routes_to_error_handler_above_max_retries(self):
        assert route_after_verify({"error": "test failed", "retry_count": MAX_RETRIES + 1}) == "error_handler"

    def test_max_retries_is_three(self):
        assert MAX_RETRIES == 3

    def test_routes_to_implementation_when_below_state_retry_budget(self):
        assert route_after_verify({"error": "test failed", "retry_count": 1, "retry_budget": 2}) == "implementation"

    def test_routes_to_error_handler_at_state_retry_budget(self):
        assert route_after_verify({"error": "test failed", "retry_count": 2, "retry_budget": 2}) == "error_handler"

    def test_invalid_state_retry_budget_falls_back_to_default(self):
        assert route_after_verify({"error": "test failed", "retry_count": 1, "retry_budget": "bad"}) == "implementation"

    def test_bool_state_retry_budget_falls_back_to_default(self):
        assert route_after_verify({"error": "test failed", "retry_count": 1, "retry_budget": True}) == "implementation"

    def test_negative_state_retry_budget_falls_back_to_default(self):
        assert route_after_verify({"error": "test failed", "retry_count": 1, "retry_budget": -1}) == "implementation"

    def test_routes_to_commit_when_no_error_despite_retries(self):
        assert route_after_verify({"error": None, "retry_count": 2}) == "commit"

    def test_routes_to_commit_when_error_is_empty_string(self):
        assert route_after_verify({"error": "", "retry_count": 1}) == "commit"

    def test_normalizes_none_retry_count_routes_to_implementation(self):
        assert route_after_verify({"error": "fail", "retry_count": None}) == "implementation"

    def test_normalizes_none_retry_count_no_error_routes_to_commit(self):
        assert route_after_verify({"retry_count": None}) == "commit"

    def test_routes_to_implementation_when_retry_count_is_non_int(self):
        assert route_after_verify({"error": "test failed", "retry_count": "bad"}) == "implementation"

    def test_routes_to_implementation_when_retry_count_is_negative(self):
        assert route_after_verify({"error": "test failed", "retry_count": -1}) == "implementation"

    def test_routes_to_implementation_when_retry_count_is_float(self):
        assert route_after_verify({"error": "test failed", "retry_count": 2.5}) == "implementation"

    def test_routes_to_implementation_when_retry_count_is_bool(self):
        assert route_after_verify({"error": "test failed", "retry_count": True}) == "implementation"
