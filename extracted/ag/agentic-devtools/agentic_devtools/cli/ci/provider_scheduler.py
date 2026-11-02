"""Workflow scheduling and eligible-PR capabilities."""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.reconciliation.models import WorkflowRun
    from agentic_devtools.cli.ci.scheduler import (
        DispatchEvent,
        EligiblePR,
    )


class _ProviderSchedulerMixin(ABC):
    """Workflow scheduling and eligible-PR capabilities."""

    def list_workflow_runs(
        self,
        workflow_id: str,
        *,
        window_hours: int = 24,
        include_dispatch_inputs: bool = False,
    ) -> list[WorkflowRun]:
        """List recent completed workflow runs for the specified workflow.

        Implementations should query the CI platform for completed runs within
        the given time window.

        Args:
            workflow_id: Workflow file name or numeric ID.
            window_hours: How far back to look for runs (in hours).
            include_dispatch_inputs: When ``True``, resolve ``inputs.pr_number``
                from per-run workflow details for ``workflow_dispatch`` runs
                that do not expose ``pull_requests[].number`` in list payloads.

        Returns:
            List of WorkflowRun instances.

        Raises:
            NotImplementedError: If the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_workflow_runs")

    def rerun_workflow(self, run_id: int) -> None:
        """Trigger a re-run of all jobs for the given workflow run.

        Args:
            run_id: The workflow run ID to re-run.

        Raises:
            NotImplementedError: If the provider does not support this operation.
            RuntimeError: If the re-run API call fails.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement rerun_workflow")

    def list_eligible_prs(self, max_prs: int | None = None) -> list[EligiblePR]:
        """List open PRs eligible for AI loop processing, in creation order.

        Applies platform-specific eligibility filters:
        - Excludes fork PRs (isCrossRepository)
        - Excludes PRs with ``ai-pr-loop-ignore`` label
        - Excludes human-blocked PRs

        Args:
            max_prs: Optional maximum number of eligible PRs to return.

        Returns:
            Sorted list (oldest-first) of EligiblePR dataclasses.

        Raises:
            NotImplementedError: If the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_eligible_prs")

    def list_eligible_prs_with_retry_liveness(self, max_prs: int | None = None) -> tuple[list[EligiblePR], bool]:
        """List scheduler-eligible PRs and whether an excluded retry needs polling."""
        return self.list_eligible_prs(max_prs=max_prs), False

    def list_supervisor_prs(self, max_prs: int | None = None) -> list[EligiblePR]:
        """List bounded open PRs for read-only supervisor scanning.

        Unlike :meth:`list_eligible_prs`, this inventory keeps human-blocked and
        audit-handoff PRs so the supervisor can classify them explicitly. It
        still excludes fork PRs and PRs carrying the ignore label.

        Args:
            max_prs: Optional maximum number of PRs to return.

        Returns:
            Sorted list (oldest-first) of EligiblePR dataclasses.

        Raises:
            NotImplementedError: If the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_supervisor_prs")

    def get_recent_dispatch_history(self, workflow: str) -> list[DispatchEvent]:
        """Get recent dispatch events for a workflow (for cursor fallback).

        Queries recent completed workflow runs and infers the dispatched PR
        number using two sources, tried in order:

        1. ``pull_requests[].number`` on the workflow run object — populated
           when the run was triggered by a pull-request event and GitHub
           associates it automatically.
        2. The run name — parsed with a ``#<number>`` pattern for runs whose
           name was set explicitly (e.g., via ``run-name`` in the workflow
           YAML) to include the PR number.

        Args:
            workflow: Workflow file name (e.g., "ai-pr-loop.yml").

        Returns:
            List of DispatchEvent instances sorted most-recent-first.

        Raises:
            NotImplementedError: If the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement get_recent_dispatch_history")

    def dispatch_workflow(self, workflow: str, inputs: dict[str, str]) -> None:
        """Dispatch a workflow_dispatch event with the given inputs.

        Args:
            workflow: Workflow file name (e.g., "ai-pr-loop.yml").
            inputs: Dictionary of input field names to values.

        Raises:
            NotImplementedError: If the provider does not support this operation.
            RuntimeError: If the dispatch fails.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement dispatch_workflow")

    def get_variable(self, name: str, *, use_writer_token: bool = False) -> str | None:
        """Read a repository Actions variable by name.

        Args:
            name: Variable name (e.g., "AI_PR_LOOP_LAST_DISPATCHED_PR").
            use_writer_token: When True, prefer the writer credential if the
                provider supports one.

        Returns:
            The variable value as a string, or None when the variable is not set.

        Raises:
            RuntimeError: If the variable cannot be read because of permission,
                availability, or transport failures.

            NotImplementedError: If the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement get_variable")

    def set_variable(self, name: str, value: str) -> None:
        """Create or update a repository Actions variable.

        Requires REPO_VARIABLE_WRITER_PAT to be configured.

        Args:
            name: Variable name (e.g., "AI_PR_LOOP_LAST_DISPATCHED_PR").
            value: Variable value to set.

        Raises:
            NotImplementedError: If the provider does not support this operation.
            VariableWriteError: When the write cannot be performed.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement set_variable")

    def validate_variable_token(self) -> bool:
        """Validate that REPO_VARIABLE_WRITER_PAT is configured and functional.

        Returns:
            True if the token is valid and has sufficient permissions, False otherwise.

        Raises:
            NotImplementedError: If the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement validate_variable_token")
