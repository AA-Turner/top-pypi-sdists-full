from __future__ import annotations

from agentic_devtools.orchestration.safety.exceptions import (
    BranchIsolationError,
    PendingOperationBlockError,
    PolicyViolationError,
    ReplayUnavailableError,
    SafetyPolicyError,
    UnclassifiedToolError,
    WorktreeIsolationError,
)


class TestExceptionHierarchy:
    """Tests for safety exception instantiation and inheritance."""

    def test_exceptions_inherit_from_safety_policy_error(self) -> None:
        assert issubclass(PolicyViolationError, SafetyPolicyError)
        assert issubclass(UnclassifiedToolError, SafetyPolicyError)
        assert issubclass(BranchIsolationError, SafetyPolicyError)
        assert issubclass(WorktreeIsolationError, SafetyPolicyError)
        assert issubclass(ReplayUnavailableError, SafetyPolicyError)
        assert issubclass(PendingOperationBlockError, SafetyPolicyError)

    def test_policy_violation_error_sets_attributes_and_message(self) -> None:
        error = PolicyViolationError("tool-a", "dry_run", "external_mutation", reason="blocked")

        assert error.tool_name == "tool-a"
        assert error.mode == "dry_run"
        assert error.classification == "external_mutation"
        assert "tool 'tool-a'" in str(error)
        assert "dry_run" in str(error)
        assert "blocked" in str(error)

    def test_policy_violation_error_without_reason(self) -> None:
        error = PolicyViolationError("tool-b", "restricted", "destructive")

        assert error.tool_name == "tool-b"
        assert "tool 'tool-b'" in str(error)
        assert "restricted" in str(error)

    def test_unclassified_tool_error_sets_tool_name(self) -> None:
        error = UnclassifiedToolError("mystery_tool")

        assert error.tool_name == "mystery_tool"
        assert "mystery_tool" in str(error)
        assert "ClassificationRegistry" in str(error)

    def test_branch_isolation_error_sets_attributes(self) -> None:
        error = BranchIsolationError("main", "main")

        assert error.branch == "main"
        assert error.pattern == "main"
        assert "protected pattern 'main'" in str(error)

    def test_worktree_isolation_error_sets_attributes(self) -> None:
        error = WorktreeIsolationError("/tmp/outside.txt", ["/repo", "/repo/subdir"])

        assert error.path == "/tmp/outside.txt"
        assert error.allowed_roots == ["/repo", "/repo/subdir"]
        assert "/repo, /repo/subdir" in str(error)

    def test_replay_unavailable_error_includes_reason(self) -> None:
        error = ReplayUnavailableError("tool:123", reason="result missing")

        assert error.operation_id == "tool:123"
        assert "tool:123" in str(error)
        assert "result missing" in str(error)

    def test_replay_unavailable_error_without_reason(self) -> None:
        error = ReplayUnavailableError("tool:789")

        assert error.operation_id == "tool:789"
        assert "tool:789" in str(error)
        assert "unavailable" in str(error)

    def test_pending_operation_block_error_sets_operation_id(self) -> None:
        error = PendingOperationBlockError("tool:456")

        assert error.operation_id == "tool:456"
        assert "tool:456" in str(error)
        assert "allow_pending_reexecute=True" in str(error)
