"""Tests for route_after_commit conditional edge function."""

from agentic_devtools.orchestration.pilot_workflow import route_after_commit


class TestRouteAfterCommit:
    def test_routes_to_pull_request_when_both_signals_true(self):
        assert route_after_commit({"commit_created": True, "branch_pushed": True}) == "pull_request"

    def test_routes_to_error_handler_when_error_present(self):
        assert route_after_commit({"error": "commit failed"}) == "error_handler"

    def test_routes_to_pull_request_legacy_fallback(self):
        """Legacy checkpoint fallback: absent signal fields route to pull_request."""
        assert route_after_commit({}) == "pull_request"

    def test_routes_to_error_handler_when_only_commit_created(self):
        assert route_after_commit({"commit_created": True, "branch_pushed": False}) == "error_handler"

    def test_routes_to_error_handler_when_only_branch_pushed(self):
        assert route_after_commit({"commit_created": False, "branch_pushed": True}) == "error_handler"

    def test_error_takes_precedence_over_signals(self):
        assert route_after_commit({"error": "boom", "commit_created": True, "branch_pushed": True}) == "error_handler"

    def test_routes_to_error_handler_when_both_false(self):
        assert route_after_commit({"commit_created": False, "branch_pushed": False}) == "error_handler"


class TestRouteAfterCommitStructuredResult:
    """route_after_commit prefers the structured CommitResult when present."""

    def test_routes_to_pull_request_on_success_commit_result(self):
        from agentic_devtools.models.git_results import CommitResult

        state = {"commit_result": CommitResult(commit_sha="abc", is_amend=False, push_succeeded=True)}
        assert route_after_commit(state) == "pull_request"

    def test_routes_to_pull_request_on_no_op_commit_result(self):
        from agentic_devtools.models.git_results import CommitResult

        # No-op (no error) still proceeds to PR per FR-008.
        state = {"commit_result": CommitResult(no_op=True, push_succeeded=False)}
        assert route_after_commit(state) == "pull_request"

    def test_routes_to_error_handler_on_blocked_commit_result(self):
        from agentic_devtools.models.git_results import BlockedState, CommitResult

        state = {"commit_result": CommitResult(error=BlockedState(category="conflict", message="rebase conflict"))}
        assert route_after_commit(state) == "error_handler"

    def test_routes_to_error_handler_on_partial_commit_result(self):
        from agentic_devtools.models.git_results import CommitResult

        # A result with no push_succeeded and no no_op (corrupt checkpoint) is rejected.
        state = {"commit_result": CommitResult()}
        assert route_after_commit(state) == "error_handler"
