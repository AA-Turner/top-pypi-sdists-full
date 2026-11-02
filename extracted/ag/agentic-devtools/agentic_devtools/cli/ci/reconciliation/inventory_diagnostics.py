"""Fail-closed live eligibility and same-scan reconciliation diagnostics."""

from dataclasses import dataclass
from enum import StrEnum
from os import environ
from pathlib import Path

from agentic_devtools.cli.ci.agent_task_inventory import (
    AgentTaskInventoryAvailability,
    AgentTaskInventoryLoadResult,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.reconciliation.models import ReconciliationAction, WorkItem
from agentic_devtools.cli.ci.scheduler_inventory_scan import SchedulerInventoryScan


class InventoryStatus(StrEnum):
    """Whether this scan can establish repository-wide task absence."""

    COMPLETE = "complete"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class LiveEligibilityChecker:
    """Use membership only when GitHub task evidence is complete."""

    eligible_numbers: frozenset[int]
    github: bool
    snapshot: SchedulerInventoryScan | None

    @property
    def status(self) -> InventoryStatus:
        """Missing and uninitialized GitHub snapshots are unknown."""
        if self.snapshot is not None and self.snapshot.availability is AgentTaskInventoryAvailability.COMPLETE:
            return InventoryStatus.COMPLETE
        return InventoryStatus.UNKNOWN

    def __call__(self, item: WorkItem) -> bool | None:
        if self.github and self.status is InventoryStatus.UNKNOWN:
            return None
        return item.pr_number in self.eligible_numbers

    def diagnostics(self) -> dict[str, str | int | None]:
        """Expose observed facts, never infer metadata from exception text."""
        if not self.github:
            return {}
        snapshot = self.snapshot
        inventory = snapshot.inventory if snapshot else None
        typed = inventory if isinstance(inventory, AgentTaskInventoryLoadResult) else None
        session = snapshot.session_diagnostics if snapshot else None
        if session:
            source = session.failure_source
            reason = session.failure_category.value if session.failure_category else None
            http_status = session.http_status
            failure_category = session.failure_category
        else:
            source = snapshot.source if snapshot else None
            reason = snapshot.reason if snapshot else None
            http_status = typed.http_status if typed else None
            failure_category = typed.failure_category if typed else None
        return {
            "inventory_status": self.status.value,
            "inventory_source": source,
            "inventory_reason": reason,
            "inventory_availability": snapshot.availability if snapshot else None,
            "inventory_http_status": http_status,
            "inventory_failure_category": failure_category,
            "inventory_row_count": len(typed.tasks)
            if typed
            else len(inventory)
            if isinstance(inventory, list)
            else None,
        }

    def summarize(self, message: str) -> str:
        """Render the same diagnostic facts in text and the GitHub step summary."""
        if not self.github:
            return message
        if self.status is InventoryStatus.UNKNOWN:
            message = (
                "Reconciliation blocked: Agent Tasks inventory unknown. "
                "No writer dispatched; a later due-work scan must obtain complete evidence."
            )
        text = "\n".join(
            f"{key}: {value if value is not None else 'unknown'}" for key, value in self.diagnostics().items()
        )
        summary_path = environ.get("GITHUB_STEP_SUMMARY")
        if summary_path:
            with Path(summary_path).open("a", encoding="utf-8") as summary:
                summary.write(f"\n### Reconciliation inventory\n\n{message}\n\n")
                summary.writelines(f"- {line}\n" for line in text.splitlines())
        return f"{message}\n{text}"


def _build_live_eligibility_checker(provider: CIPlatformProvider) -> LiveEligibilityChecker:
    """Build a checker backed by this invocation's current scheduler eligibility."""
    from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

    eligible_numbers = frozenset(candidate.number for candidate in provider.list_eligible_prs())
    snapshot = getattr(provider, "scheduler_inventory_scan", None)
    return LiveEligibilityChecker(
        eligible_numbers,
        isinstance(provider, GitHubActionsProvider),
        snapshot if isinstance(snapshot, SchedulerInventoryScan) else None,
    )


def summarize_scan(
    result: tuple[ReconciliationAction, str], checker: LiveEligibilityChecker | None
) -> tuple[ReconciliationAction, str]:
    """Attach observed inventory diagnostics without changing the dispatch action."""
    action, message = result
    return action, checker.summarize(message) if checker else message
