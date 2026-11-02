"""CI event, metadata, and agent-task capabilities."""

from __future__ import annotations

from abc import ABC, abstractmethod

from agentic_devtools.cli.ci.models import (
    AgentTaskInventory,
    AgentTaskInventoryAvailability,
    AgentTaskInventoryFailureCategory,
    AgentTaskInventoryLoadResult,
    CheckRunStatus,
    CopilotSessionSummary,
    EventPayload,
    PRMetadata,
    ReviewInfo,
)


class _ProviderEventsMixin(ABC):
    """CI event, metadata, and agent-task capabilities."""

    @abstractmethod
    def parse_event(self, raw_payload: dict, event_name: str) -> EventPayload:
        """Parse a raw CI event payload into a normalized EventPayload.

        Args:
            raw_payload: Raw JSON payload from the CI platform.
            event_name: Event type name (e.g., "pull_request", "issues").

        Returns:
            Normalized EventPayload dataclass.

        Raises:
            MalformedEventError: If the payload cannot be parsed.
        """

    @abstractmethod
    def get_pr_metadata(self, pr_number: int) -> PRMetadata:
        """Retrieve pull request metadata from the CI platform.

        Args:
            pr_number: Pull request number.

        Returns:
            PRMetadata with full PR details.
        """

    @abstractmethod
    def list_check_runs(self, head_sha: str) -> list[CheckRunStatus]:
        """List check runs for a given commit SHA.

        Args:
            head_sha: Commit SHA to query check runs for.

        Returns:
            List of CheckRunStatus for all check runs.
        """

    def is_codeql_configured(self, repo: str | None = None, *, base_branch: str = "") -> bool:
        """Return whether CodeQL is configured for the repository and PR base branch."""
        return False

    @abstractmethod
    def list_reviews(self, pr_number: int) -> list[ReviewInfo]:
        """List reviews for a pull request.

        Args:
            pr_number: Pull request number.

        Returns:
            List of ReviewInfo for all reviews.
        """

    def list_pr_session_summaries(self, pr_number: int) -> list[CopilotSessionSummary]:
        """Return completed Copilot session summaries for the given pull request."""
        return []

    def list_pr_agent_task_lifecycles(
        self,
        pr_number: int,
        *,
        pr_id: int | None = None,
        head_branch: str = "",
        head_sha: str = "",
    ) -> AgentTaskInventory:
        """Return bounded task/session evidence, marked incomplete when unsupported."""
        return AgentTaskInventory((), complete=False, incomplete_reasons=("unsupported-provider",))

    def invalidate_agent_task_inventory(self, pr_number: int | None = None) -> None:
        """Invalidate cached task/session evidence when supported by the provider."""

    def get_or_record_agent_task_first_observed_at(
        self,
        pr_number: int,
        *,
        task_id: str,
        session_id: str = "",
        head_branch: str = "",
        expected_head_sha: str = "",
    ) -> str | None:
        """Return a durable first-observed time scoped to the expected HEAD when supported."""
        return None

    def get_agent_task_first_observed_at(
        self,
        pr_number: int,
        *,
        task_id: str,
        session_id: str = "",
        head_branch: str = "",
        expected_head_sha: str = "",
    ) -> str | None:
        """Read an expected-HEAD-scoped lifecycle clock without creating provider state."""
        return None

    def get_agent_task_prompt(self, task_id: str) -> str:
        """Return the original Agent Task prompt when supported by the provider."""
        return ""

    def list_agent_tasks(self, repo: str) -> AgentTaskInventoryLoadResult:
        """Return typed task evidence, or unavailable evidence when unsupported."""
        return AgentTaskInventoryLoadResult(
            (),
            complete=False,
            incomplete_reasons=("unsupported-provider",),
            availability=AgentTaskInventoryAvailability.UNAVAILABLE,
            failure_category=AgentTaskInventoryFailureCategory.PROVIDER_UNAVAILABLE,
        )

    def dispatch_agent_retry(self, pr_number: int, prompt: str, failure_event_id: str) -> int:
        """Dispatch one failed-session retry through a provider-specific mechanism."""
        raise NotImplementedError(f"{type(self).__name__} does not implement dispatch_agent_retry")

    def _dispatch_agent_retry(self, pr_number: int, prompt: str, key: str, *, initial_delivery: bool = False) -> int:
        """Internal retry-comment route for separately fenced initial delivery."""
        raise NotImplementedError(f"{type(self).__name__} does not implement initial-delivery dispatch")
