"""Jira issue adapter wrapping ``agentic_devtools.tools.jira`` functions.

Maps Jira-specific API results to the shared adapter TypedDicts defined
in :mod:`agentic_devtools.adapters.base`.
"""

from __future__ import annotations

from typing import Any

from agentic_devtools.adapters.base import (
    Comment,
    CommentResult,
    IssueAdapter,
    IssueDetailWithRaw,
    IssueFilters,
    IssueResult,
    IssueSummary,
    IssueTypeInfo,
    NormalizedIssue,
    PropertySchema,
)
from agentic_devtools.tools.jira import JiraConfig
from agentic_devtools.tools.jira import add_comment as jira_add_comment
from agentic_devtools.tools.jira import create_issue as jira_create_issue
from agentic_devtools.tools.jira import fetch_issue_context as jira_fetch_issue_context


class JiraAdapter(IssueAdapter):
    """Issue adapter backed by Jira REST API via :mod:`agentic_devtools.tools.jira`."""

    def __init__(self, config: JiraConfig, project_key: str | None = None, issue_type: str = "Task") -> None:
        self._config = config
        self._project_key = project_key or ""
        self._issue_type = issue_type
        self._sdk_client: Any = None
        self._issue_types_cache: list[IssueTypeInfo] | None = None
        self._type_properties_cache: dict[str, list[PropertySchema]] = {}

    def _require_project_key(self) -> str:
        """Return the configured project key, raising if unset.

        Raises :class:`ValueError` when no project key is configured.
        """
        if not self._project_key:
            raise ValueError(
                "JiraAdapter requires a Jira project_key, but none was "
                "configured. Set platform.jira.project_key in configuration or pass "
                "project_key when constructing JiraAdapter."
            )
        return self._project_key

    def _ensure_sdk_client(self) -> Any:
        """Lazily create and cache the Atlassian SDK client.

        Returns the cached SDK client instance, creating it on first call
        via :func:`build_jira_client` with the adapter's config.

        Raises:
            ImportError: If ``atlassian-python-api`` is not installed.
            ValueError: If Jira base URL configuration is empty/invalid.
            OSError: If Jira authorization header is missing/empty.
        """
        if self._sdk_client is None:
            from agentic_devtools.cli.jira.sdk import build_jira_client

            self._sdk_client = build_jira_client(config=self._config)
        return self._sdk_client

    def _translate_sdk_error(self, err: Exception, operation: str) -> RuntimeError:
        """Translate SDK/requests exceptions into descriptive RuntimeError.

        Args:
            err: The caught exception.
            operation: Description of the operation that failed.

        Returns:
            A RuntimeError with actionable guidance.
        """
        import requests

        status_code: int | None = None
        url_info = ""

        if isinstance(err, requests.exceptions.Timeout):
            from agentic_devtools.cli.jira.sdk import _SDK_TIMEOUT_SECONDS

            return RuntimeError(
                f"Jira API request timed out during {operation}. "
                "Check network connectivity and Jira server availability. "
                f"The configured timeout is {_SDK_TIMEOUT_SECONDS} seconds."
            )
        if isinstance(err, requests.exceptions.ConnectionError):
            return RuntimeError(
                f"Failed to connect to Jira during {operation}. "
                f"Check that the Jira URL ({self._config.base_url}) is correct "
                "and the server is reachable."
            )
        if isinstance(err, requests.exceptions.HTTPError):
            response = getattr(err, "response", None)
            if response is not None:
                status_code = response.status_code
                url_info = f" (URL: {response.url})" if hasattr(response, "url") else ""

        # Try atlassian ApiError
        try:
            from atlassian import errors as atlassian_errors

            if isinstance(err, atlassian_errors.ApiError):
                status_code = getattr(err, "status_code", None)
        except ImportError:
            pass

        if status_code == 401:
            return RuntimeError(
                f"Jira authentication failed during {operation}{url_info} "
                f"(HTTP {status_code}). Verify your JIRA_COPILOT_PAT is valid "
                "and has the required permissions."
            )
        if status_code == 403:
            return RuntimeError(
                f"Jira authorization denied during {operation}{url_info} "
                f"(HTTP {status_code}). The configured user lacks permissions "
                "for this project."
            )
        if status_code is not None:
            return RuntimeError(f"Jira API error during {operation}{url_info} (HTTP {status_code}): {err}")

        return RuntimeError(f"Jira API error during {operation}: {err}")

    @staticmethod
    def _extract_status(fields: dict[str, Any], issue_detail: IssueDetailWithRaw) -> str:
        """Extract status using 4-step fallback chain (FR-002).

        1. raw["fields"]["status"]["name"] when status is a dict with "name"
        2. raw["fields"]["status"] when it is a non-empty string
        3. IssueDetailWithRaw["status"] typed field
        4. "unknown"
        """
        raw_status = fields.get("status")
        if isinstance(raw_status, dict):
            name = raw_status.get("name")
            if isinstance(name, str) and name.strip():
                return name.strip()
        elif isinstance(raw_status, str) and raw_status.strip():
            return raw_status.strip()

        typed_status = issue_detail.get("status")
        if isinstance(typed_status, str) and typed_status.strip():
            return typed_status.strip()

        return "unknown"

    @staticmethod
    def _extract_description(fields: dict[str, Any], issue_detail: IssueDetailWithRaw) -> str:
        """Extract description with typed-first precedence (FR-010).

        1. Use typed field when non-empty/non-whitespace
        2. Fall back to raw["fields"]["description"]
        3. Coerce ADF dicts via str(); whitespace-only → ""
        """
        typed_desc = issue_detail.get("description")
        if isinstance(typed_desc, str) and typed_desc.strip():
            return typed_desc

        raw_desc = fields.get("description")
        if raw_desc is None:
            return ""
        if isinstance(raw_desc, str):
            return raw_desc if raw_desc.strip() else ""
        # ADF or other non-string: coerce via str()
        coerced = str(raw_desc)
        return coerced if coerced.strip() else ""

    @staticmethod
    def _extract_labels(issue_detail: IssueDetailWithRaw) -> list[str]:
        """Extract labels defensively (FR-007).

        ``None`` items are skipped; all remaining items are coerced to ``str``
        so the returned list is always ``list[str]``.
        """
        labels = issue_detail.get("labels")
        if isinstance(labels, list):
            return [str(item) for item in labels if item is not None]
        return []

    @staticmethod
    def _extract_comments(issue_detail: IssueDetailWithRaw) -> list[Comment]:
        """Extract comments defensively (FR-008).

        Non-dict entries are skipped.  Each accepted dict is normalized into a
        :class:`~agentic_devtools.adapters.types.Comment` TypedDict: ``comment_id``
        falls back to a positional label (``c{n}``), and ``body``/``created_at``
        are coerced to ``str`` so callers always receive well-typed values.
        The timestamp is read from ``"created_at"`` first; if absent or ``None``,
        it falls back to the raw Jira ``"created"`` key.
        """
        raw = issue_detail.get("comments")
        if not isinstance(raw, list):
            return []
        result: list[Comment] = []
        pos = 0
        for entry in raw:
            if not isinstance(entry, dict):
                continue
            pos += 1
            id_val = entry.get("comment_id")
            if id_val is None:
                id_val = entry.get("id")
            comment_id = str(id_val).strip() if id_val is not None else f"c{pos}"
            if not comment_id:
                comment_id = f"c{pos}"
            body_raw = entry.get("body")
            body = str(body_raw) if body_raw is not None else ""
            created_raw = entry.get("created_at")
            if created_raw is None:
                created_raw = entry.get("created")
            created_at = str(created_raw) if created_raw is not None else ""
            result.append(Comment(comment_id=comment_id, body=body, created_at=created_at))
        return result

    def create_issue(self, title: str, description: str, labels: list[str] | None = None) -> IssueResult:
        """Create a Jira issue and return a shared :class:`IssueResult`."""
        project_key = self._require_project_key()
        result = jira_create_issue(
            config=self._config,
            project_key=project_key,
            summary=title,
            issue_type=self._issue_type,
            description=description,
            labels=labels or [],
        )
        return IssueResult(issue_id=result["issue_key"], url=result["url"])

    def get_issue(self, issue_id: str) -> IssueDetailWithRaw:
        """Fetch a Jira issue and return a shared :class:`IssueDetailWithRaw`."""
        ctx = jira_fetch_issue_context(config=self._config, issue_key=issue_id)
        issue = ctx["issue"]
        fields_raw = issue.get("fields")
        fields = fields_raw if isinstance(fields_raw, dict) else {}

        raw_title = fields.get("summary")
        if raw_title is None:
            title = ""
        elif isinstance(raw_title, str):
            title = raw_title
        else:
            title = str(raw_title)
        raw_description = fields.get("description")
        # Jira Cloud may return ADF (dict) instead of plain text; coerce to str.
        if raw_description is None:
            description = ""
        elif isinstance(raw_description, str):
            description = raw_description
        else:
            description = str(raw_description)
        raw_labels = fields.get("labels")
        labels = [label for label in raw_labels if isinstance(label, str)] if isinstance(raw_labels, list) else []
        status_field = fields.get("status")
        status_raw = status_field.get("name", "") if isinstance(status_field, dict) else ""
        if status_raw is None:
            status = ""
        elif isinstance(status_raw, str):
            status = status_raw
        else:
            status = str(status_raw)
        url = f"{self._config.base_url}/browse/{issue_id}"

        comment_field = fields.get("comment")
        raw_comments = comment_field.get("comments") if isinstance(comment_field, dict) else None
        if not isinstance(raw_comments, list):
            raw_comments = []
        comments: list[Comment] = []
        for c in raw_comments:
            if not isinstance(c, dict):
                continue
            raw_body = c.get("body", "")
            if not isinstance(raw_body, str):
                raw_body = "" if raw_body is None else str(raw_body)
            raw_created = c.get("created", "")
            if not isinstance(raw_created, str):
                raw_created = "" if raw_created is None else str(raw_created)
            comments.append(
                Comment(
                    comment_id=str(c.get("id", "")),
                    body=raw_body,
                    created_at=raw_created,
                )
            )

        return IssueDetailWithRaw(
            issue_id=issue_id,
            title=title,
            description=description,
            status=status,
            labels=labels,
            url=url,
            comments=comments,
            raw=issue,
        )

    def add_comment(self, issue_id: str, comment: str) -> CommentResult:
        """Add a comment to a Jira issue."""
        result = jira_add_comment(config=self._config, issue_key=issue_id, comment=comment)
        return CommentResult(comment_id=result["comment_id"])

    def list_issues(self, filters: IssueFilters | None = None) -> list[IssueSummary]:
        """Not yet implemented for Jira."""
        raise NotImplementedError("JiraAdapter.list_issues is not yet implemented. Full Jira search is a future issue.")

    def normalize(self, issue_detail: IssueDetailWithRaw) -> NormalizedIssue:
        """Normalize a Jira issue detail into a provider-agnostic representation.

        Extracts status, description, labels, comments, and created/updated dates
        from the raw Jira payload using defensive fallback chains and null handling.
        Jira-specific fields (issuetype, priority, components, customfield_*) are not
        mapped to dedicated attributes; they are preserved as-is in
        :attr:`NormalizedIssue.raw` for downstream consumers that need them.

        Additionally, when Jira's nested ``raw["fields"]["issuetype"]["name"]`` is a
        non-empty string, it is copied into a top-level ``raw["issue_type"]`` key so
        the provider-agnostic type resolver (FR-005) can read it directly. The
        caller's original ``issue_detail["raw"]`` mapping is not mutated — a shallow
        copy is made before adding the key.
        """
        raw = issue_detail.get("raw")
        raw = raw if isinstance(raw, dict) else {}
        fields = raw.get("fields")
        if not isinstance(fields, dict):
            fields = {}

        # FR-002: Status fallback chain
        status = self._extract_status(fields, issue_detail)

        # FR-010: Description with fallback
        description = self._extract_description(fields, issue_detail)

        # FR-007: Labels from typed field
        labels = self._extract_labels(issue_detail)

        # FR-008: Comments from typed field
        comments = self._extract_comments(issue_detail)

        # FR-009: Dates from raw fields
        created_at = fields.get("created", "")
        created_at = created_at if isinstance(created_at, str) else ""
        updated_at = fields.get("updated", "")
        updated_at = updated_at if isinstance(updated_at, str) else ""

        # FR-005: Normalize Jira nested issue type into top-level raw["issue_type"]
        # without mutating the caller's original raw payload.
        normalized_raw = raw
        issuetype = fields.get("issuetype")
        if isinstance(issuetype, dict):
            issuetype_name = issuetype.get("name")
            if isinstance(issuetype_name, str) and issuetype_name.strip():
                normalized_raw = dict(raw)
                normalized_raw["issue_type"] = issuetype_name

        return NormalizedIssue(
            issue_id=issue_detail["issue_id"],
            title=issue_detail["title"],
            url=issue_detail["url"],
            provider="jira",
            description=description,
            status=status,
            labels=labels,
            comments=comments,
            created_at=created_at,
            updated_at=updated_at,
            raw=normalized_raw,
        )

    def get_issue_types(self) -> list[IssueTypeInfo]:
        """Return available issue types for the Jira project.

        Uses the Jira createmeta API via the Atlassian SDK to enumerate
        issue types available in the configured project.

        Returns:
            A list of :class:`IssueTypeInfo` dicts. Returns an empty list
            when the project has no discoverable issue types.

        Raises:
            ValueError: If no project key is configured.
            ImportError: If ``atlassian-python-api`` is not installed.
            RuntimeError: On API communication errors.
        """
        if self._issue_types_cache is not None:
            return [
                IssueTypeInfo(name=item["name"], description=item["description"]) for item in self._issue_types_cache
            ]

        project_key = self._require_project_key()
        client = self._ensure_sdk_client()

        try:
            response = client.get_project_issueTypes(project_key)
        except Exception as err:
            raise self._translate_sdk_error(err, f"get_issue_types for project {project_key}") from err

        issue_types: list[IssueTypeInfo] = []
        if isinstance(response, list):
            for item in response:
                if not isinstance(item, dict):
                    continue
                raw_name = item.get("name", "")
                name = raw_name if isinstance(raw_name, str) else ("" if raw_name is None else str(raw_name))
                raw_description = item.get("description")
                description = (
                    raw_description
                    if isinstance(raw_description, str)
                    else ("" if raw_description is None else str(raw_description))
                )
                issue_types.append(IssueTypeInfo(name=name, description=description))

        self._issue_types_cache = issue_types
        return [IssueTypeInfo(name=item["name"], description=item["description"]) for item in issue_types]

    def get_type_properties(self, type_name: str) -> list[PropertySchema]:
        """Return field schema for a Jira issue type.

        Performs case-insensitive matching on the type name while preserving
        original field name casing in the returned schema.

        Args:
            type_name: The issue type name (e.g. "Bug", "Story"). Matched
                case-insensitively.

        Returns:
            A list of :class:`PropertySchema` dicts describing the fields
            available for the specified issue type.

        Raises:
            ValueError: If ``type_name`` is empty or the type does not exist
                in the configured project.
            ImportError: If ``atlassian-python-api`` is not installed.
            RuntimeError: On API communication errors.
        """
        if not type_name or not type_name.strip():
            raise ValueError(
                "type_name must not be empty. Provide a valid issue type name (e.g. 'Bug', 'Story', 'Task')."
            )

        type_name = type_name.strip()
        cache_key = type_name.lower()
        if cache_key in self._type_properties_cache:
            return [
                PropertySchema(
                    name=item["name"],
                    type=item["type"],
                    required=item["required"],
                    allowed_values=list(item["allowed_values"]) if item["allowed_values"] is not None else None,
                )
                for item in self._type_properties_cache[cache_key]
            ]

        project_key = self._require_project_key()
        client = self._ensure_sdk_client()

        # Get issue types to find the matching type ID
        try:
            issue_types_response = client.get_project_issueTypes(project_key)
        except Exception as err:
            raise self._translate_sdk_error(err, f"get_type_properties for project {project_key}") from err

        matched_type_id: str | None = None
        if isinstance(issue_types_response, list):
            for item in issue_types_response:
                if not isinstance(item, dict):
                    continue
                raw_item_name = item.get("name", "")
                item_name = (
                    raw_item_name
                    if isinstance(raw_item_name, str)
                    else ("" if raw_item_name is None else str(raw_item_name))
                )
                if item_name.lower() == cache_key:
                    raw_type_id = item.get("id")
                    if isinstance(raw_type_id, str):
                        matched_type_id = raw_type_id if raw_type_id else None
                    elif raw_type_id is None:
                        matched_type_id = None
                    else:
                        matched_type_id = str(raw_type_id)
                    break

        if matched_type_id is None:
            raise ValueError(
                f"Issue type '{type_name}' not found in project '{project_key}'. "
                "Use get_issue_types() to list available types."
            )

        # Get fields for the matched issue type
        try:
            fields_response = client.get_issue_type_fields(matched_type_id)
        except Exception as err:
            raise self._translate_sdk_error(
                err,
                f"get_type_properties for type '{type_name}' in project {project_key}",
            ) from err

        properties: list[PropertySchema] = []
        if isinstance(fields_response, dict):
            for field_key, field_meta in fields_response.items():
                if not isinstance(field_meta, dict):
                    continue
                # Use the field key as the stable provider-agnostic identifier
                # (e.g. "summary", "priority", "customfield_10001"), not the
                # locale-dependent display name from field_meta["name"].
                name = field_key
                # Determine type from schema or default to "string"
                schema = field_meta.get("schema", {})
                raw_field_type = schema.get("type") if isinstance(schema, dict) else "string"
                field_type = (
                    raw_field_type
                    if isinstance(raw_field_type, str)
                    else (str(raw_field_type) if raw_field_type else "string")
                )
                required = bool(field_meta.get("required", False))

                # Extract allowed values
                raw_allowed = field_meta.get("allowedValues")
                allowed_values: list[str] | None = None
                if isinstance(raw_allowed, list) and len(raw_allowed) > 0:
                    allowed_values = []
                    for val in raw_allowed:
                        if isinstance(val, dict):
                            # Prefer "name", fall back to "value", then "id".
                            # Use explicit `is not None` checks so that valid
                            # falsey values (e.g. 0) are not skipped, and keys
                            # that are present-but-null do not produce "None".
                            raw = next(
                                (val[k] for k in ("name", "value", "id") if k in val and val[k] is not None),
                                "",
                            )
                            allowed_values.append(str(raw))
                        else:
                            allowed_values.append(str(val))

                properties.append(
                    PropertySchema(
                        name=name,
                        type=field_type,
                        required=required,
                        allowed_values=allowed_values,
                    )
                )

        self._type_properties_cache[cache_key] = properties
        return [
            PropertySchema(
                name=item["name"],
                type=item["type"],
                required=item["required"],
                allowed_values=list(item["allowed_values"]) if item["allowed_values"] is not None else None,
            )
            for item in properties
        ]
