"""Jira issue-type operations and identifier validation."""

from __future__ import annotations

from agentic_devtools.adapters.exceptions import AdapterValidationError
from agentic_devtools.adapters.issue_provider import (
    VALID_ISSUE_TYPES,
    DefinitiveCreationFailure,
    IssueNotFoundError,
    ProviderIssueResult,
    check_hierarchy_pair,
)
from agentic_devtools.adapters.jira_provider_config import _JiraProviderMixinProtocol
from agentic_devtools.adapters.retry import retry_on_transient


class _JiraProviderIssueTypesMixin(_JiraProviderMixinProtocol):
    """Validate identifiers and update Jira issue types."""

    @retry_on_transient
    def set_issue_type(
        self,
        identifier: str,
        issue_type: str,
        *,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Validate and set the issue type on an existing Jira issue.

        Returns ``status="no-op"`` when the current type already matches the
        target after mapping.

        Raises:
            ValueError: If ``identifier`` is empty or the issue is not found.
        """
        if not identifier or not identifier.strip():
            raise ValueError("identifier must be non-empty.")
        identifier = identifier.strip()

        type_name = self._normalize_issue_type(issue_type)

        if dry_run:
            return ProviderIssueResult(
                identifier=identifier,
                url="",
                status="dry-run",
                metadata={"issue_type": type_name},
            )

        # Fetch current issue type for no-op detection
        get_url = self._api_url(f"/issue/{identifier}?fields=issuetype")
        get_resp = self._request("GET", get_url)
        if get_resp.status_code == 404:
            raise ValueError(f"Issue '{identifier}' not found.")
        get_resp.raise_for_status()
        current_data = get_resp.json()
        if not isinstance(current_data, dict):
            raise ValueError(f"Unexpected response type from Jira API: {type(current_data).__name__}")
        _fields_raw = current_data.get("fields")
        _fields = _fields_raw if isinstance(_fields_raw, dict) else {}
        _issuetype = _fields.get("issuetype")
        current_type = _issuetype.get("name", "") if isinstance(_issuetype, dict) else ""
        if current_type == type_name:
            issue_url = f"{self._base_url}/browse/{identifier}"
            return ProviderIssueResult(
                identifier=identifier,
                url=issue_url,
                status="no-op",
                metadata={"issue_type": type_name},
            )

        # Update the issue type
        url = self._api_url(f"/issue/{identifier}")
        payload = {"fields": {"issuetype": {"name": type_name}}}
        resp = self._request("PUT", url, json=payload)
        resp.raise_for_status()

        issue_url = f"{self._base_url}/browse/{identifier}"
        return ProviderIssueResult(
            identifier=identifier,
            url=issue_url,
            status="updated",
            metadata={"issue_type": type_name},
        )

    @retry_on_transient
    def resolve_identifier(
        self,
        identifier: str,
        *,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Resolve a Jira issue key to its details.

        Raises ``ValueError`` for empty/whitespace identifiers regardless of
        ``dry_run``.  On 404/not-found, raises :class:`IssueNotFoundError`
        (a ``ValueError`` subclass).  A malformed response body raises a
        plain ``ValueError`` so callers can distinguish "definitely missing"
        from "indeterminate lookup".
        """
        if not identifier or not identifier.strip():
            raise ValueError("identifier must be non-empty.")
        identifier = identifier.strip()

        if dry_run:
            return ProviderIssueResult(
                identifier=identifier,
                url="",
                status="dry-run",
                metadata={},
            )

        url = self._api_url(f"/issue/{identifier}")
        resp = self._request("GET", url)
        if resp.status_code == 404:
            raise IssueNotFoundError(f"Issue '{identifier}' not found.")
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, dict):
            raise ValueError(f"Unexpected response type from Jira API: {type(data).__name__}")

        raw_key = data.get("key")
        issue_key = raw_key.strip() if isinstance(raw_key, str) and raw_key.strip() else identifier
        issue_url = f"{self._base_url}/browse/{issue_key}"

        return ProviderIssueResult(
            identifier=issue_key,
            url=issue_url,
            status="resolved",
            metadata={"internal_id": data.get("id", "")},
        )

    def normalize_identifier(self, identifier: str) -> str:
        """Normalize a Jira issue identifier (strips surrounding whitespace).

        Raises ``ValueError`` for empty/whitespace-only identifiers.
        """
        if not identifier or not identifier.strip():
            raise ValueError("identifier must be non-empty.")
        return identifier.strip()

    def format_identifier(self, identifier: str) -> str:
        """Format a Jira issue identifier for display (strips surrounding whitespace).

        Raises ``ValueError`` for empty/whitespace-only identifiers.
        """
        if not identifier or not identifier.strip():
            raise ValueError("identifier must be non-empty.")
        return identifier.strip()

    def validate_issue_type(self, issue_type: str) -> None:
        """Validate an issue type against Jira's issue-type mapping.

        Raises:
            AdapterValidationError: If the type is unsupported or unmapped.
        """
        if not isinstance(issue_type, str) or not issue_type.strip():
            raise AdapterValidationError("issue_type must be a non-empty string")
        type_lower = issue_type.lower().strip()
        if type_lower not in VALID_ISSUE_TYPES:
            raise AdapterValidationError(
                f"Unsupported issue type '{issue_type}'. Valid types: {sorted(VALID_ISSUE_TYPES)}"
            )

    def validate_hierarchy_pair(self, child_type: str, parent_type: str) -> None:
        """Validate a parent-child issue-type pair for Jira.

        Raises:
            AdapterValidationError: If either type is unsupported or the pair is
                not a permitted parent-above-child combination.
        """
        self.validate_issue_type(child_type)
        self.validate_issue_type(parent_type)
        check_hierarchy_pair(child_type, parent_type)

    def _normalize_issue_type(self, issue_type: str) -> str:
        """Normalize an issue type to Jira's expected format.

        Validates against ``VALID_ISSUE_TYPES`` and raises ``ValueError``
        with sorted valid types for unknown types.
        """
        if not isinstance(issue_type, str) or not issue_type.strip():
            raise DefinitiveCreationFailure("issue_type must be a non-empty string")
        type_lower = issue_type.lower().strip()
        if type_lower not in VALID_ISSUE_TYPES:
            raise DefinitiveCreationFailure(
                f"Unsupported issue type '{issue_type}'. Valid types: {sorted(VALID_ISSUE_TYPES)}"
            )
        return self._effective_type_map[type_lower]
