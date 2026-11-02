"""Repository attribution and GraphQL capabilities."""

from __future__ import annotations

from abc import ABC

from agentic_devtools.cli.ci.models import PRMetadata


class _ProviderRepositoryMixin(ABC):
    """Repository attribution and GraphQL capabilities."""

    def get_commit_author_login(self, sha: str) -> str:
        """Return the GitHub login of the commit author for ``sha``.

        Returns an empty string when the provider does not support this
        operation or the author cannot be mapped to a GitHub login.

        Args:
            sha: Commit SHA to resolve.
        """
        return ""

    def list_relevant_pull_requests(
        self,
        *,
        cursor: str | None = None,
        limit: int = 25,
    ) -> tuple[list[PRMetadata], str | None]:
        """List one page of relevant open pull requests.

        Providers may override this method to expose a complete, cursor-based
        inventory.  The default keeps older providers source-compatible while
        making unsupported inventory explicit to callers.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement list_relevant_pull_requests")

    def get_pr_copilot_attribution(self, pr_number: int, *, observation_watermark: str = "") -> dict[str, bool | str]:
        """Return whether a pull request has Copilot activity after a watermark."""
        raise NotImplementedError(f"{type(self).__name__} does not implement get_pr_copilot_attribution")

    def reclaim_copilot_commit(
        self,
        *,
        pr_number: int,
        head_branch: str,
        head_sha: str,
    ) -> None:
        """Re-author the HEAD commit under the CI identity and force-push.

        Reclaims a Copilot-authored HEAD so the force-push emits a ``synchronize``
        event from a human pusher and the required ``pull_request`` checks run
        (Copilot/automation pushes are suppressed by GitHub's automation-origin
        exception to the *Require approval for workflow runs* policy).

        Args:
            pr_number: Pull request number (for logging).
            head_branch: Source branch to reclaim.
            head_sha: Current HEAD SHA (safety check before reclaim).

        Raises:
            NotImplementedError: When the provider does not support this operation.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement reclaim_copilot_commit")

    def graphql(self, *, query: str, variables: dict | None = None) -> dict:
        """Execute a GraphQL query or mutation against the GitHub API.

        Args:
            query: The GraphQL query or mutation string.
            variables: Optional dictionary of query variables.

        Returns:
            Parsed JSON response as a dictionary.

        Raises:
            NotImplementedError: If the provider does not support GraphQL.
            RetryableError: On rate limit or transient failures.
            RuntimeError: On non-retryable API errors.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement graphql")
