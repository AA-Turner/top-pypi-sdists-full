"""Jira issue-label capability."""

from __future__ import annotations

from agentic_devtools.adapters.issue_provider import ProviderIssueResult
from agentic_devtools.adapters.jira_provider_config import _JiraProviderMixinProtocol
from agentic_devtools.adapters.retry import retry_on_transient


class _JiraProviderLabelsMixin(_JiraProviderMixinProtocol):
    """Apply labels to Jira issues."""

    @retry_on_transient
    def apply_labels(
        self,
        identifier: str,
        labels: list[str],
        *,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Apply labels to a Jira issue (idempotent, additive).

        Returns ``status="no-op"`` for empty list or all already present,
        ``status="updated"`` when at least one new label is applied, or
        ``status="dry-run"`` in dry-run mode.  For non-dry-run results
        ``metadata["labels"]`` reflects the full post-operation label set; in
        dry-run mode no HTTP request is made and ``metadata["labels"]`` is a
        sorted preview of the requested labels only.
        """
        if not identifier or not identifier.strip():
            raise ValueError("identifier must be non-empty.")
        identifier = identifier.strip()

        requested_labels = list(dict.fromkeys(lbl.strip() for lbl in labels if isinstance(lbl, str) and lbl.strip()))

        if dry_run:
            # Dry-run preview: report only the requested labels (sorted, unique)
            # without issuing any HTTP request or reading existing labels.
            return ProviderIssueResult(
                identifier=identifier,
                url="",
                status="dry-run",
                metadata={"labels": sorted(set(requested_labels))},
            )

        # Fetch existing labels
        url = self._api_url(f"/issue/{identifier}?fields=labels")
        resp = self._request("GET", url)
        if resp.status_code == 404:
            raise ValueError(f"Issue '{identifier}' not found.")
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, dict):
            raise ValueError(f"Unexpected response type from Jira API: {type(data).__name__}")
        _fields_raw = data.get("fields")
        _fields = _fields_raw if isinstance(_fields_raw, dict) else {}
        labels_value = _fields.get("labels")
        existing_labels: list[str] = (
            [lbl.strip() for lbl in labels_value if isinstance(lbl, str) and lbl.strip()]
            if isinstance(labels_value, list)
            else []
        )

        if not requested_labels:
            return ProviderIssueResult(
                identifier=identifier,
                url=f"{self._base_url}/browse/{identifier}",
                status="no-op",
                metadata={"labels": sorted(existing_labels)},
            )

        new_labels = [lbl for lbl in requested_labels if lbl not in existing_labels]

        if not new_labels:
            return ProviderIssueResult(
                identifier=identifier,
                url=f"{self._base_url}/browse/{identifier}",
                status="no-op",
                metadata={"labels": sorted(existing_labels)},
            )

        # Add new labels
        update_url = self._api_url(f"/issue/{identifier}")
        update_payload = {"update": {"labels": [{"add": lbl} for lbl in new_labels]}}
        update_resp = self._request("PUT", update_url, json=update_payload)
        update_resp.raise_for_status()

        all_labels = sorted(set(existing_labels) | set(new_labels))
        return ProviderIssueResult(
            identifier=identifier,
            url=f"{self._base_url}/browse/{identifier}",
            status="updated",
            metadata={"labels": all_labels},
        )
