"""Jira orchestration-key lookup capability."""

from __future__ import annotations

from agentic_devtools.adapters.issue_provider import ProviderIssueResult
from agentic_devtools.adapters.jira_provider_config import _JiraProviderMixinProtocol
from agentic_devtools.adapters.orchestration_key import normalize_orchestration_key


class _JiraProviderIdempotencyMixin(_JiraProviderMixinProtocol):
    """Find Jira issues by orchestration key."""

    def _find_by_orchestration_key(self, orch_key: str) -> ProviderIssueResult | None:
        """Search for an existing issue via JQL with orchestration key.

        Internal helper that delegates to :meth:`find_existing_issue`.
        """
        return self.find_existing_issue(orch_key)

    def find_existing_issue(self, orchestration_key: str) -> ProviderIssueResult | None:
        """Find an issue by its embedded orchestration key via JQL search.

        Raises ValueError if multiple issues match (ambiguous state — FR-008).
        Propagates network/provider errors (FR-009).
        """
        normalized_key = normalize_orchestration_key(orchestration_key)
        result = self._search_by_orchestration_marker(normalized_key)
        if result is None and normalized_key != orchestration_key:
            result = self._search_by_orchestration_marker(orchestration_key)
        return result

    def _search_by_orchestration_marker(self, orchestration_key: str) -> ProviderIssueResult | None:
        escaped_key = orchestration_key.replace("\\", "\\\\").replace('"', '\\"')
        jql = f'project = "{self._project_key}" AND description ~ "agdt-orch-key:{escaped_key}"'
        url = self._api_url("/search")
        params = {"jql": jql, "maxResults": "10", "fields": "key,summary"}

        resp = self._request("GET", url, params=params)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, dict):
            raise ValueError(f"find_existing_issue: expected a JSON object from Jira search, got {type(data).__name__}")
        issues = data.get("issues", [])
        if not isinstance(issues, list):
            raise ValueError(f"find_existing_issue: expected 'issues' to be a list, got {type(issues).__name__}")
        if len(issues) > 1:
            ids = [issue.get("key", "") if isinstance(issue, dict) else repr(issue) for issue in issues]
            raise ValueError(
                f"Ambiguous state: orchestration key {orchestration_key!r} "
                f"matched {len(issues)} issues: {ids}. "
                f"Resolve manually before re-running."
            )
        if issues:
            issue = issues[0]
            if not isinstance(issue, dict):
                raise ValueError(
                    f"find_existing_issue: expected issue entry to be a JSON object, got {type(issue).__name__}"
                )
            issue_key = issue.get("key", "")
            if not isinstance(issue_key, str) or not issue_key.strip():
                raise ValueError(
                    f"find_existing_issue: expected issue 'key' to be a non-empty string, got {issue_key!r}"
                )
            return ProviderIssueResult(
                identifier=issue_key,
                url=f"{self._base_url}/browse/{issue_key}",
                status="existing",
                metadata={"id": issue.get("id", "")},
            )
        return None
