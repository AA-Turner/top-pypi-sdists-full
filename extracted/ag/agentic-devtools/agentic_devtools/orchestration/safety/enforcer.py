"""Safety enforcer — orchestrates all safety checks before tool execution.

The ``SafetyEnforcer`` is the central coordination point that applies
mode enforcement, idempotency checks, isolation guards, and audit
emission before allowing a tool to execute.
"""

from __future__ import annotations

import dataclasses
import logging
from typing import Any

from .classification import ActionClassification, ClassificationRegistry
from .exceptions import (
    PendingOperationBlockError,
    PolicyViolationError,
    ReplayUnavailableError,
)
from .isolation import BranchIsolationGuard, WorktreeIsolationGuard
from .mode import ExecutionMode
from .operation_id import compute_operation_id
from .operation_log import OperationLog, OperationLogRecord

logger = logging.getLogger(__name__)

_DUPLICATE_SKIP_REASON = "duplicate: prior completed record found"


@dataclasses.dataclass
class SafetyDecision:
    """The outcome of a safety evaluation.

    Attributes:
        action: One of "execute", "skip_duplicate", "simulate", "block".
        reason: Human-readable explanation for the decision.
        operation_id: The computed operation ID (for external mutations).
        replay_record: The prior record to replay (for skip_duplicate).
    """

    action: str
    reason: str = ""
    operation_id: str | None = None
    replay_record: OperationLogRecord | None = None


@dataclasses.dataclass
class SafetyPolicy:
    """Configuration for the safety enforcer.

    Attributes:
        execution_mode: The resolved execution mode.
        protected_branches: Branch patterns that cannot be mutated.
        allow_destructive: Whether destructive tools are permitted.
        allow_pending_reexecute: Whether to override pending-block.
        allow_replay_fallback_reexecute: Whether to re-execute when replay unavailable.
    """

    execution_mode: ExecutionMode = ExecutionMode.live
    protected_branches: list[str] = dataclasses.field(default_factory=lambda: ["main", "master"])
    allow_destructive: bool = False
    allow_pending_reexecute: bool = False
    allow_replay_fallback_reexecute: bool = False


class SafetyEnforcer:
    """Orchestrates all safety checks for tool invocations.

    Evaluation order:
    1. Classify tool (fail if unclassified)
    2. Apply mode enforcement (FR-003)
    3. Destructive opt-in gate (FR-009)
    4. Branch isolation (FR-007)
    5. Worktree isolation (FR-008)
    6. Idempotency check (FR-005)
    7. Emit audit entry
    """

    def __init__(
        self,
        policy: SafetyPolicy,
        classification_registry: ClassificationRegistry,
        operation_log: OperationLog | None = None,
        branch_guard: BranchIsolationGuard | None = None,
        worktree_guard: WorktreeIsolationGuard | None = None,
    ) -> None:
        self._policy = policy
        self._classification_registry = classification_registry
        self._operation_log = operation_log
        self._branch_guard = branch_guard or BranchIsolationGuard(policy.protected_branches)
        self._worktree_guard = worktree_guard or WorktreeIsolationGuard()

    @property
    def policy(self) -> SafetyPolicy:
        """Return the current safety policy configuration."""
        return self._policy

    @property
    def operation_log(self) -> OperationLog | None:
        """Return the operation log instance."""
        return self._operation_log

    def evaluate(self, tool_name: str, inputs: dict[str, Any] | None = None, *, node_name: str = "") -> SafetyDecision:
        """Evaluate whether a tool invocation is permitted.

        Args:
            tool_name: Name of the tool to evaluate.
            inputs: Tool invocation inputs.
            node_name: The graph node invoking the tool. Required for
                external-mutation and destructive tools (FR-006).

        Returns a SafetyDecision indicating the action to take.

        Raises:
            UnclassifiedToolError: Tool not in classification registry.
            PolicyViolationError: Mode/classification conflict.
            BranchIsolationError: Git mutation on protected branch.
            WorktreeIsolationError: File write outside allowed roots.
            PendingOperationBlockError: Prior pending operation blocks retry.
            ReplayUnavailableError: Cannot replay prior result.
            ValueError: node_name is empty for external-mutation/destructive tools.
        """
        if inputs is None:
            inputs = {}

        # Step 1: Classify tool
        entry = self._classification_registry.get(tool_name)
        classification = entry.classification
        mode = self._policy.execution_mode

        # Step 2: Mode enforcement (FR-003)
        decision = self._enforce_mode(tool_name, classification, mode)
        if decision is not None:
            return decision

        # Step 3: Destructive opt-in gate (FR-009)
        if classification == ActionClassification.destructive and not self._policy.allow_destructive:
            raise PolicyViolationError(
                tool_name,
                mode.value,
                classification.value,
                reason="destructive tools require explicit allow_destructive=True",
            )

        # Step 4: Branch isolation (FR-007)
        self._branch_guard.check(tool_name, inputs)

        # Step 5: Worktree isolation (FR-008)
        self._worktree_guard.check(tool_name, inputs)

        # Step 6: Idempotency check (FR-005) with node_name validation (FR-006)
        operation_id: str | None = None
        if classification in (
            ActionClassification.external_mutation,
            ActionClassification.destructive,
        ):
            if not node_name.strip():
                raise ValueError(
                    f"node_name must be non-empty when evaluating external-mutation or "
                    f"destructive tool '{tool_name}' — omitting it would cause cross-node "
                    f"operation_id collisions (FR-006)."
                )
            operation_id = compute_operation_id(node_name, tool_name, inputs, entry.nondeterministic_fields)
            decision = self._check_idempotency(operation_id, tool_name, node_name)
            if decision is not None:
                return decision

        # All checks passed — allow execution
        return SafetyDecision(action="execute", reason="all safety checks passed", operation_id=operation_id)

    def record_pending(self, tool_name: str, inputs: dict[str, Any], operation_id: str, *, node_name: str = "") -> None:
        """Record a pending operation before execution begins."""
        if self._operation_log is None:
            return
        record = OperationLogRecord(
            operation_id=operation_id,
            run_id=self._operation_log.run_id,
            tool_name=tool_name,
            node_name=node_name,
            input_hash=operation_id.split(":")[-1] if ":" in operation_id else "",
            execution_timestamp=self._operation_log.get_timestamp(),
            execution_mode=self._policy.execution_mode.value,
            status="pending",
        )
        self._operation_log.append(record)

    def record_completed(
        self,
        operation_id: str,
        tool_name: str,
        result_summary: str = "",
        result_payload: Any = None,
        *,
        node_name: str = "",
    ) -> None:
        """Record a completed operation after successful execution."""
        if self._operation_log is None:
            return
        record = OperationLogRecord(
            operation_id=operation_id,
            run_id=self._operation_log.run_id,
            tool_name=tool_name,
            node_name=node_name,
            execution_timestamp=self._operation_log.get_timestamp(),
            execution_mode=self._policy.execution_mode.value,
            status="completed",
            result_summary=result_summary,
            result_payload=result_payload,
        )
        self._operation_log.append(record)

    def record_failed(self, operation_id: str, tool_name: str, error_message: str = "", *, node_name: str = "") -> None:
        """Record a failed operation."""
        if self._operation_log is None:
            return
        record = OperationLogRecord(
            operation_id=operation_id,
            run_id=self._operation_log.run_id,
            tool_name=tool_name,
            node_name=node_name,
            execution_timestamp=self._operation_log.get_timestamp(),
            execution_mode=self._policy.execution_mode.value,
            status="failed",
            result_summary=error_message,
        )
        self._operation_log.append(record)

    def _enforce_mode(
        self,
        tool_name: str,
        classification: ActionClassification,
        mode: ExecutionMode,
    ) -> SafetyDecision | None:
        """Apply mode enforcement rules (FR-003).

        Returns a SafetyDecision if the mode blocks/simulates execution,
        or None if execution should proceed.
        """
        if mode == ExecutionMode.restricted:
            # Only read_only allowed in restricted mode
            if classification != ActionClassification.read_only:
                raise PolicyViolationError(
                    tool_name,
                    mode.value,
                    classification.value,
                    reason="restricted mode only permits read_only operations",
                )
            return None

        if mode == ExecutionMode.dry_run:
            # external_mutation and destructive are simulated
            if classification in (
                ActionClassification.external_mutation,
                ActionClassification.destructive,
            ):
                return SafetyDecision(
                    action="simulate",
                    reason=f"dry_run mode: {classification.value} tool simulated",
                )
            # read_only and local_mutation proceed normally
            return None

        # live mode: all classifications proceed (destructive gate handled separately)
        return None

    def _check_idempotency(
        self,
        operation_id: str,
        tool_name: str,
        node_name: str = "",
    ) -> SafetyDecision | None:
        """Check the operation log for duplicate/pending status.

        Returns a SafetyDecision if the operation should be skipped/blocked,
        or None if execution should proceed.
        """
        if self._operation_log is None:
            return None

        prior = self._operation_log.lookup(operation_id)

        if prior is None:
            # No prior record — proceed (caller should record_pending)
            return None

        if prior.status == "completed" or (prior.status == "skipped" and prior.skip_reason == _DUPLICATE_SKIP_REASON):
            # Duplicate-skip: replay prior result
            if prior.result_payload is None and not self._policy.allow_replay_fallback_reexecute:
                raise ReplayUnavailableError(operation_id, "result_payload is None")
            if prior.result_payload is None and self._policy.allow_replay_fallback_reexecute:
                # Allow re-execution as fallback
                return None

            # Append skipped record with node_name (FR-006) and
            # prior_completion_timestamp (FR-005) for audit traceability.
            # Propagate the original completion timestamp: if prior is itself a
            # skipped-duplicate record it already carries the original timestamp in
            # prior_completion_timestamp; use that to avoid drift across chains.
            original_completion_ts = (
                prior.prior_completion_timestamp
                if prior.prior_completion_timestamp is not None
                else prior.execution_timestamp
            )
            skipped = OperationLogRecord(
                operation_id=operation_id,
                run_id=self._operation_log.run_id,
                tool_name=tool_name,
                node_name=node_name,
                execution_timestamp=self._operation_log.get_timestamp(),
                execution_mode=self._policy.execution_mode.value,
                status="skipped",
                skip_reason=_DUPLICATE_SKIP_REASON,
                result_payload=prior.result_payload,
                prior_completion_timestamp=original_completion_ts,
            )
            self._operation_log.append(skipped)
            return SafetyDecision(
                action="skip_duplicate",
                reason="duplicate operation: replaying prior result",
                operation_id=operation_id,
                replay_record=prior,
            )

        if prior.status == "pending":
            # Pending-block
            if not self._policy.allow_pending_reexecute:
                raise PendingOperationBlockError(operation_id)
            # Override: allow re-execution
            return None

        if prior.status == "failed":
            # Failed prior: allow retry
            return None

        # Any other status (e.g., skipped): allow execution
        return None
