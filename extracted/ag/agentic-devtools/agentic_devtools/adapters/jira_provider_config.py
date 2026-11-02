"""Jira provider configuration and session setup."""

from __future__ import annotations

import base64
import os
from collections.abc import Callable
from typing import Any, Protocol

import requests as requests_lib

from agentic_devtools.adapters.issue_provider import (
    VALID_ISSUE_TYPES,
    PreCreateLookup,
    ProviderIssueResult,
    ProviderLinkResult,
)

# Canonical neutral key -> default Jira issue type name mapping.
# Keys must be members of VALID_ISSUE_TYPES.
_JIRA_ISSUE_TYPE_DEFAULTS: dict[str, str] = {
    "epic": "Epic",
    "feature": "Story",
    "subtask": "Sub-task",
    "task": "Task",
    "bug": "Bug",
}


class _JiraProviderMixinProtocol(Protocol):
    """Type the shared members available on ``self`` across composed provider mixins."""

    _project_key: str
    _base_url: str
    _session: requests_lib.Session
    _epic_link_field: str | None
    _dry_run_issues: list[dict[str, Any]]
    _dry_run_deps: list[dict[str, Any]]
    _idempotency_keys: dict[str, ProviderIssueResult]
    _effective_type_map: dict[str, str]
    _api_url: Callable[[str], str]
    _request: Callable[..., requests_lib.Response]
    _get_epic_link_field: Callable[[], str]
    _is_field_inapplicable_error: Callable[[requests_lib.Response, str], bool]
    _normalize_issue_type: Callable[[str], str]
    _find_by_orchestration_key: Callable[[str], ProviderIssueResult | None]
    normalize_identifier: Callable[[str], str]
    link_subissue: Callable[..., ProviderLinkResult]
    _validate_precreate_lookup: Callable[[str | None, PreCreateLookup | None], None]
    _find_existing_issue: Callable[..., ProviderIssueResult | None]
    _request_issue_creation: Callable[
        [str, str, dict[str, object]],
        tuple[requests_lib.Response | None, ProviderIssueResult | None],
    ]


class _JiraProviderConfigMixin(_JiraProviderMixinProtocol):
    """Configure Jira provider settings and its HTTP session."""

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
