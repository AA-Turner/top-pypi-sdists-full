"""Jira parent-child issue linking capability."""

from __future__ import annotations

from typing import Any

from agentic_devtools.adapters.issue_provider import ProviderLinkResult
from agentic_devtools.adapters.jira_provider_config import _JiraProviderMixinProtocol
from agentic_devtools.adapters.retry import retry_on_transient


class _JiraProviderHierarchyMixin(_JiraProviderMixinProtocol):
    """Link parent and child Jira issues."""

    @retry_on_transient
    def link_subissue(
        self,
        parent_id: str,
        child_id: str,
        *,
        dry_run: bool = False,
    ) -> ProviderLinkResult:
        """Link a child issue to a parent via epic-link or parent field.

        Idempotent: returns ``status="already-linked"`` when the child already
        has ``parent_id`` set via the epic-link field or the ``parent`` field,
        without performing any write.

        On 400/422 from the epic-link PUT, inspects the response body for
        "not applicable" indicators before falling back to the ``parent``
        field; other 400/422 failures are surfaced immediately.
        """
        if not parent_id or not parent_id.strip():
            raise ValueError("parent_id must be non-empty.")
        if not child_id or not child_id.strip():
            raise ValueError("child_id must be non-empty.")
        parent_id = parent_id.strip()
        child_id = child_id.strip()

        if dry_run:
            entry = {
                "source": parent_id,
                "target": child_id,
                "type": "sub-issue",
                "operation": f"PUT {self._base_url}/rest/api/2/issue/{child_id}",
                "status": "dry-run",
            }
            self._dry_run_deps.append(entry)
            return ProviderLinkResult(
                source_id=parent_id,
                target_id=child_id,
                status="dry-run",
            )

        # Resolve the epic-link custom field once (cached after first call).
        # Idempotency check via find_existing_link (FR-003)
        existing = self.find_existing_link(parent_id, child_id)
        if existing is not None:
            return existing

        epic_field = self._get_epic_link_field()
        url = self._api_url(f"/issue/{child_id}")
        payload = {"fields": {epic_field: parent_id}}
        epic_resp = self._request("PUT", url, json=payload)

        if epic_resp.status_code == 404:
            raise ValueError(f"Issue '{child_id}' not found.")
        if epic_resp.status_code in {400, 422}:
            # Check if this is a "field not applicable" error before falling back
            if self._is_field_inapplicable_error(epic_resp, epic_field):
                # Fall back to parent field for inapplicable-field errors
                parent_payload: dict[str, Any] = {"fields": {"parent": {"key": parent_id}}}
                fallback_resp = self._request("PUT", url, json=parent_payload)
                if fallback_resp.status_code == 404:
                    raise ValueError(f"Issue '{child_id}' not found.")
                fallback_resp.raise_for_status()
            else:
                # Surface original Jira error for other 400/422 failures
                epic_resp.raise_for_status()
        else:
            epic_resp.raise_for_status()

        return ProviderLinkResult(
            source_id=parent_id,
            target_id=child_id,
            status="linked",
        )

    def find_existing_link(self, parent_provider_id: str, child_provider_id: str) -> ProviderLinkResult | None:
        """Check if a parent-child link already exists (FR-003).

        GETs the child issue and inspects epic-link and parent fields.
        Returns ProviderLinkResult with status="already-linked" if found,
        None if not found. Propagates network errors (FR-009).
        """
        epic_field = self._get_epic_link_field()
        get_url = self._api_url(f"/issue/{child_provider_id}?fields={epic_field},parent")
        get_resp = self._request("GET", get_url)
        if get_resp.status_code == 404:
            return None
        get_resp.raise_for_status()
        get_data = get_resp.json()
        if not isinstance(get_data, dict):
            raise ValueError(f"find_existing_link: expected a JSON object from Jira, got {type(get_data).__name__}")
        _fields_raw = get_data.get("fields")
        get_fields = _fields_raw if isinstance(_fields_raw, dict) else {}
        if get_fields.get(epic_field) == parent_provider_id:
            return ProviderLinkResult(
                source_id=parent_provider_id,
                target_id=child_provider_id,
                status="already-linked",
            )
        parent_field_val = get_fields.get("parent")
        if isinstance(parent_field_val, dict) and parent_field_val.get("key") == parent_provider_id:
            return ProviderLinkResult(
                source_id=parent_provider_id,
                target_id=child_provider_id,
                status="already-linked",
            )
        return None
