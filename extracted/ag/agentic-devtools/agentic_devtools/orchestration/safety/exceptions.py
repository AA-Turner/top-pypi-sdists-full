"""Exception hierarchy for the execution safety policy.

Defines a standalone ``SafetyPolicyError(RuntimeError)`` hierarchy that is
parallel to — not inheriting from — existing orchestration exceptions.
"""

from __future__ import annotations


class SafetyPolicyError(RuntimeError):
    """Base exception for all safety policy violations."""


class PolicyViolationError(SafetyPolicyError):
    """Raised when an action violates the current execution mode policy."""

    def __init__(self, tool_name: str, mode: str, classification: str, reason: str = "") -> None:
        self.tool_name = tool_name
        self.mode = mode
        self.classification = classification
        msg = (
            f"Policy violation: tool {tool_name!r} (classification={classification}) is not permitted in {mode!r} mode"
        )
        if reason:
            msg += f": {reason}"
        super().__init__(msg)


class UnclassifiedToolError(SafetyPolicyError):
    """Raised when a tool has no classification entry in the registry."""

    def __init__(self, tool_name: str) -> None:
        self.tool_name = tool_name
        super().__init__(
            f"Tool {tool_name!r} has no safety classification entry. "
            f"All tools must be registered in the ClassificationRegistry before invocation."
        )


class BranchIsolationError(SafetyPolicyError):
    """Raised when a git mutation targets a protected branch."""

    def __init__(self, branch: str, pattern: str) -> None:
        self.branch = branch
        self.pattern = pattern
        super().__init__(
            f"Branch isolation violation: current branch {branch!r} "
            f"matches protected pattern {pattern!r}. "
            f"Autonomous workflows must not mutate protected branches."
        )


class WorktreeIsolationError(SafetyPolicyError):
    """Raised when a file operation targets a path outside allowed roots."""

    def __init__(self, path: str, allowed_roots: list[str]) -> None:
        self.path = path
        self.allowed_roots = allowed_roots
        roots_str = ", ".join(allowed_roots) if allowed_roots else "(none)"
        super().__init__(f"Worktree isolation violation: path {path!r} is outside allowed roots: {roots_str}")


class ReplayUnavailableError(SafetyPolicyError):
    """Raised when a duplicate-skip cannot replay the prior result."""

    def __init__(self, operation_id: str, reason: str = "") -> None:
        self.operation_id = operation_id
        msg = f"Cannot replay result for operation {operation_id!r}: prior result payload unavailable"
        if reason:
            msg += f" ({reason})"
        super().__init__(msg)


class PendingOperationBlockError(SafetyPolicyError):
    """Raised when a prior pending operation blocks re-execution."""

    def __init__(self, operation_id: str) -> None:
        self.operation_id = operation_id
        super().__init__(
            f"Operation {operation_id!r} has a pending record from a prior attempt. "
            f"Re-execution is blocked by default because the operation may have completed "
            f"externally. Set allow_pending_reexecute=True to override."
        )
