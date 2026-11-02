"""Support helpers for lifecycle reconciliation in the session detector."""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

from agentic_devtools.cli.ci.agent_task_inventory import inventory_failure_result
from agentic_devtools.cli.ci.models import AgentTaskInventory, AgentTaskInventoryAvailability, FailureCategory
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.pipeline.session_detector import SessionState

LIFECYCLE_RECONCILIATION_EXCEPTIONS = (
    RuntimeError,
    OSError,
    ValueError,
    TypeError,
    subprocess.TimeoutExpired,
    ProviderRateLimitError,
    RetryableError,
)


def _session_failure_metadata(exc: Exception) -> tuple[FailureCategory, int | None]:
    """Preserve the shared inventory failure classification and HTTP status."""
    failure = inventory_failure_result(exc)
    return failure.failure_category or FailureCategory.PROVIDER_UNAVAILABLE, failure.http_status


def read_reconciliation_lifecycle_inventory(
    provider: CIPlatformProvider,
    pr_number: int,
    *,
    pr_id: int | None,
    head_branch: str,
    head_sha: str,
) -> AgentTaskInventory | SessionState:
    """Read the lifecycle inventory directly from the provider for reconciliation."""
    try:
        if pr_id is None:
            return provider.list_pr_agent_task_lifecycles(pr_number, head_branch=head_branch, head_sha=head_sha)
        return provider.list_pr_agent_task_lifecycles(
            pr_number, pr_id=pr_id, head_branch=head_branch, head_sha=head_sha
        )
    except LIFECYCLE_RECONCILIATION_EXCEPTIONS as exc:
        if isinstance(exc, (RetryableError, ProviderRateLimitError)) and exc.is_rate_limit:
            raise
        category, status = _session_failure_metadata(exc)
        if category is FailureCategory.HTTP_NOT_FOUND and status == 404:
            from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState

            return SessionState(
                SessionOutcome.UNKNOWN,
                inventory_availability=AgentTaskInventoryAvailability.UNAVAILABLE,
                failure_category=category,
                http_status=status,
                failure_source="agent-task-lifecycle",
            )
        raise
