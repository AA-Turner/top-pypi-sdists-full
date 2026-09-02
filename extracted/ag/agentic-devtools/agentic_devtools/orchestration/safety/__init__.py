"""Execution safety policy for autonomous workflows.

Public API exports for the ``agentic_devtools.orchestration.safety`` package.
"""

from .classification import (
    ActionClassification,
    ClassificationEntry,
    ClassificationRegistry,
    build_default_registry,
)
from .enforcer import SafetyDecision, SafetyEnforcer, SafetyPolicy
from .exceptions import (
    BranchIsolationError,
    PendingOperationBlockError,
    PolicyViolationError,
    ReplayUnavailableError,
    SafetyPolicyError,
    UnclassifiedToolError,
    WorktreeIsolationError,
)
from .isolation import BranchIsolationGuard, WorktreeIsolationGuard
from .mode import (
    ExecutionMode,
    persist_execution_mode,
    resolve_execution_mode,
    resolve_execution_mode_from_state,
    validate_mode_on_resume,
)
from .operation_id import compute_operation_id
from .operation_log import OperationLog, OperationLogRecord
from .query import query_operation_log, read_audit_entries

__all__ = [
    "ActionClassification",
    "BranchIsolationError",
    "BranchIsolationGuard",
    "ClassificationEntry",
    "ClassificationRegistry",
    "ExecutionMode",
    "OperationLog",
    "OperationLogRecord",
    "PendingOperationBlockError",
    "PolicyViolationError",
    "ReplayUnavailableError",
    "SafetyDecision",
    "SafetyEnforcer",
    "SafetyPolicy",
    "SafetyPolicyError",
    "UnclassifiedToolError",
    "WorktreeIsolationError",
    "WorktreeIsolationGuard",
    "build_default_registry",
    "compute_operation_id",
    "persist_execution_mode",
    "query_operation_log",
    "read_audit_entries",
    "resolve_execution_mode",
    "resolve_execution_mode_from_state",
    "validate_mode_on_resume",
]
