"""Jira IssueProvider implementation.

Uses the ``requests`` library for REST API calls, with authentication
following the existing patterns from ``agentic_devtools.tools.jira``.

Conforms to the :class:`~agentic_devtools.adapters.issue_provider.IssueProvider`
protocol (8 methods with keyword-only ``dry_run``).  The ``issue_type_map``
constructor parameter allows instance-specific Jira issue-type name overrides
(e.g., German-localized names) without hard-coding English names.
"""

from __future__ import annotations

import base64
import copy
import os
from typing import Any

import requests as requests_lib

from agentic_devtools.adapters.dry_run_manifest import build_dry_run_manifest
from agentic_devtools.adapters.exceptions import AdapterValidationError
from agentic_devtools.adapters.issue_provider import (
    VALID_ISSUE_TYPES,
    ProviderIssueResult,
    ProviderLinkResult,
    check_hierarchy_pair,
)
from agentic_devtools.adapters.orchestration_key import extract_orchestration_key
from agentic_devtools.adapters.retry import TransientError, retry_on_transient

# Canonical neutral key -> default Jira issue type name mapping.
# Keys must be members of VALID_ISSUE_TYPES.
_JIRA_ISSUE_TYPE_DEFAULTS: dict[str, str] = {
    "epic": "Epic",
    "feature": "Story",
    "subtask": "Sub-task",
    "task": "Task",
    "bug": "Bug",
}
_DEFAULT_TIMEOUT_SECONDS = 30

# Jira custom field for the required "Epic Name" field on Epic issues
_EPIC_NAME_FIELD = "customfield_10006"


class JiraProvider:
    """Jira IssueProvider using the Jira REST API v2.

    Conforms to the
    :class:`~agentic_devtools.adapters.issue_provider.IssueProvider` protocol.

    Args:
        project_key: Jira project key (e.g., ``"PROJ"``).  Must be non-empty.
        base_url: Jira instance base URL.  Falls back to ``JIRA_BASE_URL`` env.
            Must be resolvable (non-empty after resolution).
        session: Optional ``requests.Session`` for testing injection.
        issue_type_map: Optional mapping of canonical neutral type keys
            (members of ``VALID_ISSUE_TYPES``) to Jira-native issue-type names.
            Overrides default mappings; unspecified keys fall back to built-in
            defaults.  Values must be non-empty, non-whitespace strings.
    """

    def __init__(
        self,
        project_key: str,
        base_url: str | None = None,
        session: requests_lib.Session | None = None,
        issue_type_map: dict[str, str] | None = None,
    ) -> None:
        if not project_key or not project_key.strip():
            raise ValueError("project_key must be non-empty.")
        self._project_key = project_key.strip()

        resolved_url = (base_url or os.environ.get("JIRA_BASE_URL", "")).strip().rstrip("/")
        if not resolved_url:
            raise ValueError(
                "Jira base URL is not configured. "
                "Set the JIRA_BASE_URL environment variable or pass base_url to JiraProvider."
            )
        self._base_url = resolved_url

        self._session = session or self._build_session()
        self._epic_link_field: str | None = None
        self._dry_run_issues: list[dict[str, Any]] = []
        self._dry_run_deps: list[dict[str, Any]] = []
        self._idempotency_keys: dict[str, ProviderIssueResult] = {}

        # Validate and build effective type map
        if issue_type_map is not None:
            for key, value in issue_type_map.items():
                if not isinstance(key, str):
                    raise ValueError(f"issue_type_map key must be a string, got {type(key).__name__}: {key!r}")
                key_lower = key.lower().strip()
                if key_lower not in VALID_ISSUE_TYPES:
                    raise ValueError(
                        f"issue_type_map key '{key}' (normalized: '{key_lower}') is not a valid "
                        f"canonical type. Valid keys: {sorted(VALID_ISSUE_TYPES)}"
                    )
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(
                        f"issue_type_map value for key '{key}' must be a non-empty, "
                        f"non-whitespace string, got {value!r}"
                    )
        self._effective_type_map = self._build_effective_type_map(issue_type_map)

    @property
    def project_key(self) -> str:
        """Return the configured project key."""
        return self._project_key

    # ------------------------------------------------------------------
    # Session construction
    # ------------------------------------------------------------------

    def _build_session(self) -> requests_lib.Session:
        """Build a requests session with Jira authentication."""
        session = requests_lib.Session()
        session.headers["Content-Type"] = "application/json"

        token = os.environ.get("JIRA_API_TOKEN", "") or os.environ.get("JIRA_COPILOT_PAT", "")
        identity = (
            os.environ.get("JIRA_USER_EMAIL", "")
            or os.environ.get("JIRA_EMAIL", "")
            or os.environ.get("JIRA_USERNAME", "")
        )
        auth_scheme = os.environ.get("JIRA_AUTH_SCHEME", "bearer").lower()

        if identity or auth_scheme == "basic":
            if identity and token:
                credentials = base64.b64encode(f"{identity}:{token}".encode()).decode()
                session.headers["Authorization"] = f"Basic {credentials}"
        elif token:
            session.headers["Authorization"] = "Bearer " + token

        # SSL verification
        ssl_env = os.environ.get("JIRA_SSL_VERIFY", "")
        if ssl_env.lower() in ("0", "false"):
            session.verify = False
        elif ssl_env:
            session.verify = ssl_env
        else:
            ca_bundle = os.environ.get("JIRA_CA_BUNDLE", "") or os.environ.get("REQUESTS_CA_BUNDLE", "")
            session.verify = ca_bundle if ca_bundle else True

        return session

    @staticmethod
    def _build_effective_type_map(
        custom_map: dict[str, str] | None,
    ) -> dict[str, str]:
        """Merge custom overrides onto defaults and return the effective map."""
        merged = dict(_JIRA_ISSUE_TYPE_DEFAULTS)
        if custom_map:
            merged.update({k.lower().strip(): v.strip() for k, v in custom_map.items()})
        return merged

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _api_url(self, path: str) -> str:
        """Build a full Jira REST API URL."""
        return f"{self._base_url}/rest/api/2{path}"

    def _request(self, method: str, url: str, **kwargs: Any) -> requests_lib.Response:
        """Make an HTTP request, raising on transient errors."""
        kwargs.setdefault("timeout", _DEFAULT_TIMEOUT_SECONDS)
        resp = self._session.request(method, url, **kwargs)
        if resp.status_code in (429, 502, 503):
            raise TransientError(
                f"Jira API returned {resp.status_code}: {resp.text[:200]}",
                status_code=resp.status_code,
            )
        return resp

    def _get_epic_link_field(self) -> str:
        """Dynamically resolve the epic-link custom field ID.

        Queries ``GET /rest/api/2/field`` and searches for a field whose
        name or schema contains "epic link".
        """
        if self._epic_link_field:
            return self._epic_link_field

        url = self._api_url("/field")
        resp = self._request("GET", url)
        resp.raise_for_status()
        fields = resp.json()

        for f in fields:
            name = (f.get("name") or "").lower()
            schema = f.get("schema", {})
            custom_type = (schema.get("custom", "") or "").lower() if isinstance(schema, dict) else ""
            if "epic link" in name or "epiclink" in custom_type or "epic-link" in custom_type:
                self._epic_link_field = f["id"]
                return self._epic_link_field

        # Fallback to common field ID
        self._epic_link_field = "customfield_10008"
        return self._epic_link_field

    @staticmethod
    def _is_field_inapplicable_error(response: requests_lib.Response, field_name: str) -> bool:
        """Return True when a Jira validation error indicates a field is inapplicable."""
        field_name_lower = field_name.lower()
        field_error_indicators = (
            "not on the appropriate screen",
            "not applicable",
            "cannot be set",
            "does not exist",
        )
        try:
            payload = response.json()
        except ValueError:
            payload = None

        if isinstance(payload, dict):
            errors = payload.get("errors")
            if isinstance(errors, dict):
                field_error = errors.get(field_name)
                if isinstance(field_error, str):
                    field_error_lower = field_error.lower()
                    return any(indicator in field_error_lower for indicator in field_error_indicators)

            error_messages = payload.get("errorMessages")
            if isinstance(error_messages, list):
                for message in error_messages:
                    if not isinstance(message, str):
                        continue
                    message_lower = message.lower()
                    if field_name_lower in message_lower and any(
                        indicator in message_lower for indicator in field_error_indicators
                    ):
                        return True

        response_text = (response.text or "").lower()
        for line in response_text.splitlines():
            if field_name_lower in line and any(indicator in line for indicator in field_error_indicators):
                return True
        return False

    # ------------------------------------------------------------------
    # IssueProvider protocol methods
    # ------------------------------------------------------------------

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
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Create a Jira issue with native issue types.

        The ``idempotency_key`` deduplication cache is scoped to this provider
        instance and lives in memory for the lifetime of the object.  A cached
        key returns a new result with ``status="existing"`` — the
        ``identifier``, ``url``, and ``metadata`` fields are preserved from
        the original creation result, while only ``status`` is changed to
        ``"existing"`` so orchestrators can distinguish a dedup hit from a
        true creation.  For cross-run idempotency, use orchestration keys
        embedded in the body.

        Args:
            title: Issue summary.  Must be non-empty after stripping whitespace.
            body: Issue description body.
            issue_type: Provider-neutral type (member of ``VALID_ISSUE_TYPES``).
            parent_id: Optional parent issue key for hierarchy linking.
            labels: Optional list of label strings to include at creation time.
            idempotency_key: Optional deduplication key.
            dry_run: When ``True``, skip mutations and return a preview result.

        Returns:
            A :class:`ProviderIssueResult` with status ``"created"``,
            ``"existing"``, or ``"dry-run"``.

        Raises:
            ValueError: If title is empty, issue_type is unsupported, or
                parent_id is provided but empty.
        """
        if not title or not title.strip():
            raise ValueError("title must be non-empty.")
        if parent_id is not None and not parent_id.strip():
            raise ValueError("parent_id must be a non-empty string when provided.")
        if parent_id is not None:
            parent_id = parent_id.strip()
        if idempotency_key is not None:
            idempotency_key = idempotency_key.strip()
            if not idempotency_key:
                idempotency_key = None

        operation = f"POST {self._base_url}/rest/api/2/issue"

        # Validate issue_type mapping eagerly — including in dry-run — so previews match execution.
        type_name = self._normalize_issue_type(issue_type)

        if dry_run:
            entry = {
                "title": title,
                "issue_type": issue_type,
                "operation": operation,
                "status": "dry-run",
                "parent_id": parent_id,
            }
            self._dry_run_issues.append(entry)
            return ProviderIssueResult(
                identifier="",
                url="",
                status="dry-run",
                metadata={"operation": operation, "title": title},
            )

        # Idempotency: in-memory deduplication via idempotency_key
        if idempotency_key is not None and idempotency_key in self._idempotency_keys:
            cached = self._idempotency_keys[idempotency_key]
            return ProviderIssueResult(
                identifier=cached.identifier,
                url=cached.url,
                status="existing",
                metadata=copy.deepcopy(cached.metadata),
            )

        # Idempotency: find-before-create via orchestration key
        orch_key = extract_orchestration_key(body)
        if orch_key:
            existing = self._find_by_orchestration_key(orch_key)
            if existing:
                return existing

        # Build the issue creation payload
        canonical = issue_type.lower().strip()
        fields: dict[str, Any] = {
            "project": {"key": self._project_key},
            "summary": title,
            "description": body,
            "issuetype": {"name": type_name},
        }

        # Epic Name (customfield_10006) is required by Jira for Epic issues.
        # Key off the canonical neutral type ("epic"), not the Jira-native name, so
        # that custom type maps (e.g. {"epic": "Epos"}) still populate this field.
        if canonical == "epic":
            fields[_EPIC_NAME_FIELD] = title

        # Include labels at creation time when provided and non-empty.
        # Normalize the incoming list to strip whitespace, remove empty values,
        # ignore non-string entries, and preserve first-seen order.
        normalized_labels = (
            list(dict.fromkeys(lbl.strip() for lbl in labels if isinstance(lbl, str) and lbl.strip()))
            if labels is not None
            else []
        )
        if normalized_labels:
            fields["labels"] = normalized_labels

        # Handle parent linking at creation time using the canonical key so that
        # custom type maps (e.g. {"subtask": "Teilaufgabe"}) are handled correctly.
        if parent_id:
            if canonical == "subtask":
                fields["parent"] = {"key": parent_id}
            elif canonical != "epic":
                # Link to epic via epic-link field
                epic_field = self._get_epic_link_field()
                fields[epic_field] = parent_id

        url = self._api_url("/issue")
        resp = self._request("POST", url, json={"fields": fields})
        resp.raise_for_status()
        data = resp.json()

        if not isinstance(data, dict):
            raise ValueError(f"Unexpected response type from Jira API: {type(data).__name__}")

        issue_key = data.get("key", "")
        if not isinstance(issue_key, str) or not issue_key.strip():
            raise ValueError(f"Jira API response did not include a valid issue key: {data!r}")
        issue_key = issue_key.strip()
        issue_url = f"{self._base_url}/browse/{issue_key}"

        result = ProviderIssueResult(
            identifier=issue_key,
            url=issue_url,
            status="created",
            metadata={"id": data.get("id", "")},
        )

        # Store result under idempotency key for future lookups
        if idempotency_key is not None:
            self._idempotency_keys[idempotency_key] = ProviderIssueResult(
                identifier=result.identifier,
                url=result.url,
                status=result.status,
                metadata=copy.deepcopy(result.metadata),
            )

        return result

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
        ``dry_run``.  On 404/not-found, raises ``ValueError``.
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
            raise ValueError(f"Issue '{identifier}' not found.")
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

    # ------------------------------------------------------------------
    # Hierarchy-validation capability (HierarchyValidationProvider)
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _normalize_issue_type(self, issue_type: str) -> str:
        """Normalize an issue type to Jira's expected format.

        Validates against ``VALID_ISSUE_TYPES`` and raises ``ValueError``
        with sorted valid types for unknown types.
        """
        type_lower = issue_type.lower().strip()
        if type_lower not in VALID_ISSUE_TYPES:
            raise ValueError(f"Unsupported issue type '{issue_type}'. Valid types: {sorted(VALID_ISSUE_TYPES)}")
        return self._effective_type_map[type_lower]

    def _find_by_orchestration_key(self, orch_key: str) -> ProviderIssueResult | None:
        """Search for an existing issue via JQL with orchestration key.

        Internal helper that delegates to :meth:`find_existing_issue`.
        """
        return self.find_existing_issue(orch_key)

    # ------------------------------------------------------------------
    # IdempotencyQueryProvider methods
    # ------------------------------------------------------------------

    def find_existing_issue(self, orchestration_key: str) -> ProviderIssueResult | None:
        """Find an issue by its embedded orchestration key via JQL search.

        Raises ValueError if multiple issues match (ambiguous state — FR-008).
        Propagates network/provider errors (FR-009).
        """
        jql = f'project = "{self._project_key}" AND description ~ "agdt-orch-key:{orchestration_key}"'
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

    # ------------------------------------------------------------------
    # Dry-run manifest
    # ------------------------------------------------------------------

    def get_dry_run_manifest(self) -> dict[str, Any]:
        """Return the accumulated dry-run manifest."""
        return build_dry_run_manifest(
            issues=self._dry_run_issues,
            dependencies=self._dry_run_deps,
        )
