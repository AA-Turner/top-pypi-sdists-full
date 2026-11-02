"""GitHub orchestration-key lookup operations."""

from __future__ import annotations

from agentic_devtools.adapters.github_provider_common import _GitHubProviderCommonMixin
from agentic_devtools.adapters.issue_provider import ProviderIssueResult
from agentic_devtools.adapters.orchestration_key import normalize_orchestration_key


class GitHubProviderIdempotencyMixin(_GitHubProviderCommonMixin):
    def find_existing_issue(self, orchestration_key: str) -> ProviderIssueResult | None:
        """Find an issue by its orchestration key via the provider query capability."""
        return self._find_by_orchestration_key(orchestration_key)

    def _find_by_orchestration_key(self, orch_key: str) -> ProviderIssueResult | None:
        """Search for an existing issue with the given orchestration key.

        Returns a result with ``status="existing"`` when a match is found, or
        ``None`` when the search succeeds but returns no results.  Any search
        failure (authentication errors, malformed responses, transient errors,
        or a match lacking a valid positive issue ``number``) is propagated to
        the caller rather than silently treated as "not found", which would
        cause duplicate issues to be created on re-runs.
        """
        normalized_key = normalize_orchestration_key(orch_key)
        result = self._search_by_orchestration_marker(normalized_key)
        if result is None and normalized_key != orch_key:
            result = self._search_by_orchestration_marker(orch_key)
        return result

    def _search_by_orchestration_marker(self, orch_key: str) -> ProviderIssueResult | None:
        query_key = orch_key.replace("\\", "\\\\").replace('"', '\\"')
        query = f'repo:{self._owner_repo} "agdt-orch-key:{query_key}" in:body is:issue'
        args = [
            "gh",
            "api",
            "/search/issues",
            "--method",
            "GET",
            "-f",
            f"q={query}",
        ]
        result = self._exec_gh(args)
        data = self._parse_json(result.stdout)
        if not isinstance(data, dict):
            raise RuntimeError("Expected search response object from GitHub issue search.")
        if data.get("incomplete_results") is True:
            raise RuntimeError(
                "GitHub issue search timed out and returned incomplete results; "
                "cannot safely determine idempotent-create status."
            )
        items = data.get("items", [])
        if not isinstance(items, list):
            raise RuntimeError("Expected search response items to be a list.")
        if len(items) > 1:
            raise RuntimeError(
                f"Ambiguous idempotency-key search: {len(items)} issues matched "
                f"orchestration key {orch_key!r}. Cannot safely determine which "
                "issue to treat as the existing one."
            )
        if items:
            item = items[0]
            if not isinstance(item, dict):
                raise RuntimeError("Expected first search result item to be an object.")
            number = item.get("number")
            if not isinstance(number, int) or isinstance(number, bool) or number <= 0:
                raise RuntimeError("GitHub issue search result did not include a valid positive issue number.")
            return ProviderIssueResult(
                identifier=str(number),
                url=item.get("html_url", ""),
                status="existing",
                metadata={
                    "database_id": item.get("id", 0),
                    "node_id": item.get("node_id", ""),
                },
            )
        return None
