"""Jira issue-creation result construction."""

from __future__ import annotations

import copy
from typing import Any

from agentic_devtools.adapters.exceptions import HierarchyLinkError
from agentic_devtools.adapters.issue_provider import ProviderIssueResult, ProviderLinkResult
from agentic_devtools.adapters.jira_provider_config import _JiraProviderMixinProtocol


class _JiraProviderCreationResultsMixin(_JiraProviderMixinProtocol):
    """Build consistent results for created and recovered Jira issues."""

    def _build_created_issue_result(
        self,
        response: Any,
        idempotency_key: str | None,
        parent_id: str | None,
        canonical_type: str,
    ) -> ProviderIssueResult:
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError(f"Unexpected response type from Jira API: {type(data).__name__}")
        issue_key = data.get("key", "")
        if not isinstance(issue_key, str) or not issue_key.strip():
            raise ValueError(f"Jira API response did not include a valid issue key: {data!r}")
        issue_key = issue_key.strip()
        result = ProviderIssueResult(
            identifier=issue_key,
            url=f"{self._base_url}/browse/{issue_key}",
            status="created",
            metadata={"id": data.get("id", "")},
            hierarchy_link_result=(
                ProviderLinkResult(source_id=parent_id.strip(), target_id=issue_key, status="linked")
                if parent_id and canonical_type != "epic"
                else None
            ),
        )
        if idempotency_key is not None:
            self._idempotency_keys[idempotency_key] = ProviderIssueResult(
                identifier=result.identifier,
                url=result.url,
                status=result.status,
                metadata=copy.deepcopy(result.metadata),
            )
        return result

    def _build_recovered_issue_result(
        self,
        recovered: ProviderIssueResult,
        idempotency_key: str | None,
        parent_id: str | None,
        canonical_type: str,
    ) -> ProviderIssueResult:
        result = ProviderIssueResult(
            identifier=recovered.identifier,
            url=recovered.url,
            status="existing",
            metadata=copy.deepcopy(recovered.metadata),
        )
        if idempotency_key is not None:
            self._idempotency_keys[idempotency_key] = result
        if parent_id is None or canonical_type == "epic":
            return result
        try:
            hierarchy_link_result = self.link_subissue(parent_id, recovered.identifier, dry_run=False)
        except Exception as link_exc:
            raise HierarchyLinkError(
                f"Issue {recovered.identifier} already exists at {recovered.url} but linking to "
                f"parent {parent_id} failed (see chained exception for details)",
                created_result=result,
                stage="link_subissue",
                cause=link_exc,
            ) from link_exc
        result = ProviderIssueResult(
            identifier=recovered.identifier,
            url=recovered.url,
            status="existing",
            metadata=copy.deepcopy(recovered.metadata),
            hierarchy_link_result=hierarchy_link_result,
        )
        if idempotency_key is not None:
            self._idempotency_keys[idempotency_key] = result
        return result
