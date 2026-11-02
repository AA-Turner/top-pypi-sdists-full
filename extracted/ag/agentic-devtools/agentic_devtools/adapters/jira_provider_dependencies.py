"""Jira blocking dependency capability."""

from __future__ import annotations

from typing import Any

from agentic_devtools.adapters.issue_provider import ProviderLinkResult
from agentic_devtools.adapters.jira_provider_config import _JiraProviderMixinProtocol
from agentic_devtools.adapters.retry import retry_on_transient


class _JiraProviderDependenciesMixin(_JiraProviderMixinProtocol):
    """Create Jira issue-blocking links."""

    @retry_on_transient
    def add_blocked_by(
        self,
        issue_id: str,
        blocked_by_id: str,
        *,
        dry_run: bool = False,
    ) -> ProviderLinkResult:
        """Create a "Blocks" issue link between two Jira issues.

        Uses the protocol parameter name ``blocked_by_id`` (renamed from the
        pre-protocol ``blocker_id``).

        Raises:
            ValueError: If either identifier is empty, or if ``issue_id ==
                blocked_by_id`` (self-blocking).
        """
        if not issue_id or not issue_id.strip():
            raise ValueError("issue_id must be a non-empty string.")
        if not blocked_by_id or not blocked_by_id.strip():
            raise ValueError("blocked_by_id must be a non-empty string.")
        issue_id = issue_id.strip()
        blocked_by_id = blocked_by_id.strip()
        if issue_id == blocked_by_id:
            raise ValueError(f"Self-blocking is not allowed: issue_id and blocked_by_id are both '{issue_id}'.")

        if dry_run:
            entry = {
                "source": blocked_by_id,
                "target": issue_id,
                "type": "blocks",
                "operation": f"POST {self._base_url}/rest/api/2/issueLink",
                "status": "dry-run",
            }
            self._dry_run_deps.append(entry)
            return ProviderLinkResult(
                source_id=blocked_by_id,
                target_id=issue_id,
                status="dry-run",
            )

        url = self._api_url("/issueLink")
        # Idempotency check via find_existing_dependency (FR-004)
        existing = self.find_existing_dependency(issue_id, blocked_by_id)
        if existing is not None:
            return existing

        payload = {
            "type": {"name": "Blocks"},
            "inwardIssue": {"key": issue_id},
            "outwardIssue": {"key": blocked_by_id},
        }
        resp = self._request("POST", url, json=payload)
        if resp.status_code == 404:
            detail = resp.text.strip()
            detail_suffix = f". Response: {detail}" if detail else "."
            raise ValueError(
                f"Blocked-by link failed because one or both issues were not found: "
                f"issue_id='{issue_id}', blocked_by_id='{blocked_by_id}'{detail_suffix}"
            )
        resp.raise_for_status()

        return ProviderLinkResult(
            source_id=blocked_by_id,
            target_id=issue_id,
            status="linked",
        )

    def find_existing_dependency(
        self, issue_provider_id: str, blocked_by_provider_id: str
    ) -> ProviderLinkResult | None:
        """Check if a blocking dependency already exists (FR-004).

        GETs the issue's links and checks for a "Blocks" outward link
        to blocked_by_provider_id. Returns ProviderLinkResult with
        status="already-linked" if found, None if not found.
        Propagates network errors (FR-009).
        """
        get_url = self._api_url(f"/issue/{issue_provider_id}?fields=issuelinks")
        get_resp = self._request("GET", get_url)
        if get_resp.status_code == 404:
            return None
        get_resp.raise_for_status()
        get_data = get_resp.json()
        if not isinstance(get_data, dict):
            raise ValueError(
                f"find_existing_dependency: expected a JSON object from Jira, got {type(get_data).__name__}"
            )
        _fields_raw = get_data.get("fields")
        fields = _fields_raw if isinstance(_fields_raw, dict) else {}
        existing_links_raw = fields.get("issuelinks")
        if existing_links_raw is None:
            existing_links: list[Any] = []
        elif isinstance(existing_links_raw, list):
            existing_links = existing_links_raw
        else:
            raise ValueError(
                "find_existing_dependency: expected fields.issuelinks to be a list when present, "
                f"got {type(existing_links_raw).__name__}"
            )
        for link in existing_links:
            if not isinstance(link, dict):
                continue
            link_type = link.get("type")
            if not isinstance(link_type, dict):
                continue
            if (link_type.get("name") or "").lower() == "blocks":
                _raw_outward = link.get("outwardIssue")
                outward = _raw_outward if isinstance(_raw_outward, dict) else {}
                if outward.get("key") == blocked_by_provider_id:
                    return ProviderLinkResult(
                        source_id=blocked_by_provider_id,
                        target_id=issue_provider_id,
                        status="already-linked",
                    )
        return None
