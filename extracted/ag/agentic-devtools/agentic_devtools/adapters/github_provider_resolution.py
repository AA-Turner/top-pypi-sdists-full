"""GitHub issue identifier resolution."""

from __future__ import annotations

from agentic_devtools.adapters.github_provider_common import _NOT_FOUND_RE, _GitHubProviderCommonMixin
from agentic_devtools.adapters.issue_provider import IssueNotFoundError, ProviderIssueResult
from agentic_devtools.adapters.retry import retry_on_transient


class GitHubProviderResolutionMixin(_GitHubProviderCommonMixin):
    def _resolve_identifier_inner(self, identifier_normalized: str) -> ProviderIssueResult:
        """Perform the actual identifier → database-ID lookup without a retry decorator.

        Callers that need retry behaviour should use the public
        :meth:`resolve_identifier` method.  Callers that are themselves
        already retry-decorated (``link_subissue``, ``_to_db_id``) call this
        helper directly so that a persistent transient failure does not trigger
        nested retry amplification (``4 × 4 = 16`` attempts).

        Raises ``ValueError`` when the issue is not found (GitHub HTTP 404),
        matching the :class:`IssueProvider` contract so that every caller
        (``link_subissue``, ``_to_db_id``, ``resolve_identifier``) gets
        consistent not-found behaviour without needing individual wrappers.
        Not-found raises the :class:`IssueNotFoundError` subclass so callers
        can distinguish a definitive miss from other validation failures.

        Validates that the resolved ``database_id`` is a positive integer
        before returning ``status="resolved"``, so callers see a clear error
        instead of a truthy ``"0"`` string that would silently fail later.
        """
        args = [
            "gh",
            "api",
            f"/repos/{self._owner_repo}/issues/{identifier_normalized}",
        ]
        try:
            result = self._exec_gh(args)
        except RuntimeError as exc:
            if _NOT_FOUND_RE.search(str(exc)):
                raise IssueNotFoundError(f"GitHub issue {identifier_normalized!r} not found") from exc
            raise
        data = self._parse_json(result.stdout)

        if not isinstance(data, dict):
            raise RuntimeError(f"Expected a JSON object from GitHub issues endpoint, got {type(data).__name__}")

        raw_id = data.get("id")
        if not isinstance(raw_id, int) or isinstance(raw_id, bool) or raw_id <= 0:
            raise RuntimeError(
                f"GitHub issue {identifier_normalized!r} did not return a valid positive integer "
                f"database ID; got: {raw_id!r}"
            )

        url = data.get("html_url", "")
        node_id = data.get("node_id", "")

        return ProviderIssueResult(
            identifier=identifier_normalized,
            url=url,
            status="resolved",
            metadata={
                "database_id": raw_id,
                "node_id": node_id,
                "internal_id": str(raw_id),
            },
        )

    @retry_on_transient
    def resolve_identifier(
        self,
        identifier: str,
        *,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Resolve an existing GitHub issue number to its database ID.

        Raises :class:`IssueNotFoundError` when the issue does not exist
        (GitHub returns ``HTTP 404``), matching the :class:`IssueProvider`
        contract and the Jira/InMemory adapters, so protocol consumers can
        handle a confirmed not-found result consistently and distinctly from
        any other validation failure.  The 404→``IssueNotFoundError``
        translation is performed inside :meth:`_resolve_identifier_inner`;
        other provider failures propagate unchanged.
        """
        identifier_normalized = self._normalize_issue_number(identifier, "identifier")

        if dry_run:
            return ProviderIssueResult(
                identifier=identifier_normalized,
                url="",
                status="dry-run",
            )

        return self._resolve_identifier_inner(identifier_normalized)
