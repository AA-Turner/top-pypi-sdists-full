"""GitHub issue creation operations."""

from __future__ import annotations

from agentic_devtools.adapters.github_provider_creation_helpers import _GitHubProviderCreationHelpersMixin
from agentic_devtools.adapters.issue_provider import PreCreateLookup, ProviderIssueResult
from agentic_devtools.adapters.retry import retry_on_transient


# The facade composes sibling mixins supplying the intentionally ignored members below.
class GitHubProviderCreationMixin(_GitHubProviderCreationHelpersMixin):
    @retry_on_transient
    def create_issue(
        self,
        title: str,
        body: str,
        issue_type: str,
        *,
        parent_id: str | None = None,
        labels: list[str] | None = None,
        idempotency_key: str | None = None,
        precreate_lookup: PreCreateLookup | None = None,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Create a GitHub issue via ``gh api``.

        Returns the integer database ID (``id`` field) and GraphQL ``node_id``
        in metadata for follow-up link operations.  When ``idempotency_key`` is
        provided the key is embedded in the body and a find-before-create search
        returns any existing match with ``status="existing"``.  A supplied
        ``precreate_lookup`` reuses the orchestrator's preceding result for the
        same key rather than repeating that search.
        """
        context = self._prepare_creation_context(
            title,
            body,
            issue_type,
            parent_id,
            idempotency_key,
            precreate_lookup,
        )
        if dry_run:
            return self._dry_run_creation_result(context)
        existing = self._find_existing_creation(context)
        if existing is not None:
            return existing

        payload_labels = self._creation_labels(context.type_label, labels)
        payload = {"title": context.title, "body": context.body, "labels": payload_labels}

        args = [
            "gh",
            "api",
            f"/repos/{self._owner_repo}/issues",
            "--method",
            "POST",
            "--input",
            "-",
        ]
        result, recovered = self._create_issue_with_recovery(  # type: ignore[attr-defined]
            args, payload, context.lookup_key
        )
        if recovered is not None:
            return self._recovered_creation_result(recovered, context)
        assert result is not None
        issue_result = self._created_issue_result(result.stdout, payload_labels)
        issue_result = self._link_created_issue(  # type: ignore[attr-defined]
            issue_result, context.parent_id, newly_created=True
        )
        self._cache_created_issue(issue_result, context.orchestration_key)
        return issue_result

    def create_issue_with_precreate_lookup(
        self,
        title: str,
        body: str,
        issue_type: str,
        *,
        parent_id: str | None = None,
        labels: list[str] | None = None,
        idempotency_key: str | None = None,
        precreate_lookup: PreCreateLookup,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Create an issue using a supplied pre-create lookup."""
        return self.create_issue(
            title,
            body,
            issue_type,
            parent_id=parent_id,
            labels=labels,
            idempotency_key=idempotency_key,
            precreate_lookup=precreate_lookup,
            dry_run=dry_run,
        )
