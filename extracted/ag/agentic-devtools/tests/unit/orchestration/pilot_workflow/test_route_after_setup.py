"""Tests for route_after_setup conditional edge function."""

from agentic_devtools.orchestration.pilot_workflow import route_after_setup


class TestRouteAfterSetup:
    def test_routes_to_error_handler_when_error_present(self):
        assert route_after_setup({"error": "setup failed"}) == "error_handler"

    def test_routes_to_retrieve_when_setup_complete(self):
        assert route_after_setup({"setup_complete": True}) == "retrieve"

    def test_routes_to_retrieve_when_legacy_state_has_no_signal(self):
        assert route_after_setup({}) == "retrieve"

    def test_routes_to_error_handler_when_setup_complete_false(self):
        assert route_after_setup({"setup_complete": False}) == "error_handler"


class TestRouteAfterSetupStructuredResult:
    """route_after_setup prefers the structured SetupResult when present."""

    def test_routes_to_retrieve_on_success_setup_result(self):
        from agentic_devtools.models.git_results import SetupResult

        state = {"setup_result": SetupResult(worktree_path="/wt", branch_name="feature/42/x", mode="created")}
        assert route_after_setup(state) == "retrieve"

    def test_routes_to_error_handler_on_blocked_setup_result(self):
        from agentic_devtools.models.git_results import BlockedState, SetupResult

        state = {"setup_result": SetupResult(error=BlockedState(category="transient", message="fetch failed"))}
        assert route_after_setup(state) == "error_handler"

    def test_setup_result_success_ignores_legacy_error_field(self):
        from agentic_devtools.models.git_results import SetupResult

        # Structured result takes precedence over a stale legacy error string.
        state = {
            "setup_result": SetupResult(worktree_path="/wt", branch_name="feature/42/x", mode="resumed"),
            "error": "stale",
        }
        assert route_after_setup(state) == "retrieve"

    def test_routes_to_error_handler_on_partial_setup_result(self):
        from agentic_devtools.models.git_results import SetupResult

        # A result with no worktree_path/branch_name (corrupt checkpoint) is rejected.
        state = {"setup_result": SetupResult(mode="created")}
        assert route_after_setup(state) == "error_handler"

    def test_routes_to_error_handler_when_only_mode_is_set(self):
        from agentic_devtools.models.git_results import SetupResult

        state = {"setup_result": SetupResult(worktree_path="/wt", branch_name=None, mode="created")}
        assert route_after_setup(state) == "error_handler"
