"""SpecKit pipeline retry & reconciliation logic.

Provides a reusable, provider-abstracted reconciliation engine that retries
failed workflow runs and escalates when retry limits are reached.
"""

from agentic_devtools.cli.ci.reconciliation.config import (
    MAX_RUN_ATTEMPTS,
    RECONCILIATION_WINDOW_HOURS,
    RETRIABLE_CONCLUSIONS,
)
from agentic_devtools.cli.ci.reconciliation.dispatch import (
    DispatchConflictError,
    DispatchResult,
    acquire_dispatch_claim,
    dispatch_due_work,
    evaluate_dispatch_eligibility,
    evaluate_eligibility,
    select_due_work,
)
from agentic_devtools.cli.ci.reconciliation.engine import reconcile
from agentic_devtools.cli.ci.reconciliation.exceptions import UnmappableContextError
from agentic_devtools.cli.ci.reconciliation.models import (
    ReconciliationAction,
    ReconciliationResult,
    RunEventContext,
    WorkflowRun,
)
from agentic_devtools.cli.ci.reconciliation.recovery import (
    RecoveryExhaustedError,
    confirm_recovery,
    enforce_retry_limit,
    handle_pagination_exhaustion,
    reclaim_leases,
    record_provider_failure,
    rehydrate_state,
)

__all__ = [
    "DispatchConflictError",
    "DispatchResult",
    "MAX_RUN_ATTEMPTS",
    "RECONCILIATION_WINDOW_HOURS",
    "RETRIABLE_CONCLUSIONS",
    "ReconciliationAction",
    "ReconciliationResult",
    "RecoveryExhaustedError",
    "RunEventContext",
    "UnmappableContextError",
    "WorkflowRun",
    "acquire_dispatch_claim",
    "confirm_recovery",
    "dispatch_due_work",
    "enforce_retry_limit",
    "evaluate_dispatch_eligibility",
    "evaluate_eligibility",
    "handle_pagination_exhaustion",
    "reconcile",
    "reclaim_leases",
    "record_provider_failure",
    "rehydrate_state",
    "select_due_work",
]
