"""Jira issue creation capability."""

from __future__ import annotations

from typing import Any

from agentic_devtools.adapters.issue_provider import (
    DefinitiveCreationFailure,
    PreCreateLookup,
    ProviderIssueResult,
)
from agentic_devtools.adapters.jira_provider_creation_results import _JiraProviderCreationResultsMixin
from agentic_devtools.adapters.orchestration_key import (
    embed_orchestration_key,
    extract_orchestration_key,
    normalize_orchestration_key,
)
from agentic_devtools.adapters.retry import retry_on_transient

_EPIC_NAME_FIELD = "customfield_10006"


class _JiraProviderCreationMixin(_JiraProviderCreationResultsMixin):
    """Create Jira issues with idempotency and hierarchy support."""

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
        """Create a Jira issue, optionally recovering or linking an existing issue.

        Raises:
            DefinitiveCreationFailure: If title, parent, issue type, or lookup data is invalid.
        """
        parent_id, idempotency_key = self._validate_creation_inputs(title, parent_id, idempotency_key, precreate_lookup)
        lookup_orchestration_key = idempotency_key
        if idempotency_key is not None:
            idempotency_key = normalize_orchestration_key(idempotency_key)
            body = embed_orchestration_key(body, idempotency_key)
        operation = f"POST {self._base_url}/rest/api/2/issue"
        type_name = self._normalize_issue_type(issue_type)
        if dry_run:
            return self._record_dry_run(title, issue_type, operation, parent_id)

        orchestration_key = idempotency_key or extract_orchestration_key(body)
        lookup_key = lookup_orchestration_key or orchestration_key or ""
        existing = self._find_existing_issue(
            idempotency_key, precreate_lookup, orchestration_key, lookup_key, parent_id
        )
        if existing is not None:
            return existing

        canonical_type = issue_type.lower().strip()
        fields = self._build_issue_fields(title, body, type_name, canonical_type, labels, parent_id)
        response, recovered = self._request_issue_creation(lookup_key, self._api_url("/issue"), fields)
        if recovered is not None:
            return self._build_recovered_issue_result(recovered, idempotency_key, parent_id, canonical_type)
        assert response is not None
        return self._build_created_issue_result(response, idempotency_key, parent_id, canonical_type)

    def _validate_creation_inputs(
        self,
        title: str,
        parent_id: str | None,
        idempotency_key: str | None,
        precreate_lookup: PreCreateLookup | None,
    ) -> tuple[str | None, str | None]:
        if not isinstance(title, str) or not title.strip():
            raise DefinitiveCreationFailure("title must be non-empty.")
        if parent_id is not None and (not isinstance(parent_id, str) or not parent_id.strip()):
            raise DefinitiveCreationFailure("parent_id must be a non-empty string when provided.")
        if parent_id is not None:
            parent_id = parent_id.strip()
        if idempotency_key is not None:
            idempotency_key = idempotency_key.strip() or None
        self._validate_precreate_lookup(idempotency_key, precreate_lookup)
        return parent_id, idempotency_key

    def _record_dry_run(
        self,
        title: str,
        issue_type: str,
        operation: str,
        parent_id: str | None,
    ) -> ProviderIssueResult:
        self._dry_run_issues.append(
            {
                "title": title,
                "issue_type": issue_type,
                "operation": operation,
                "status": "dry-run",
                "parent_id": parent_id,
            }
        )
        return ProviderIssueResult(
            identifier="",
            url="",
            status="dry-run",
            metadata={"operation": operation, "title": title},
        )

    def _build_issue_fields(
        self,
        title: str,
        body: str,
        type_name: str,
        canonical_type: str,
        labels: list[str] | None,
        parent_id: str | None,
    ) -> dict[str, Any]:
        fields: dict[str, Any] = {
            "project": {"key": self._project_key},
            "summary": title,
            "description": body,
            "issuetype": {"name": type_name},
        }
        if canonical_type == "epic":
            fields[_EPIC_NAME_FIELD] = title
        normalized_labels = (
            list(dict.fromkeys(label.strip() for label in labels if isinstance(label, str) and label.strip()))
            if labels is not None
            else []
        )
        if normalized_labels:
            fields["labels"] = normalized_labels
        if parent_id:
            if canonical_type == "subtask":
                fields["parent"] = {"key": parent_id}
            elif canonical_type != "epic":
                fields[self._get_epic_link_field()] = parent_id
        return fields

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
