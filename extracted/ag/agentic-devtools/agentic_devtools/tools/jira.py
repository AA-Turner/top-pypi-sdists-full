"""Jira tool adapter functions.

Stateless, typed functions for Jira operations. Each function accepts a
``JiraConfig`` for authentication and returns a ``TypedDict`` result.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from urllib.parse import quote

from typing_extensions import TypedDict

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class JiraConfig:
    """Configuration required to call the Jira REST API.

    Attributes:
        base_url: Jira instance base URL, e.g. ``https://jira.example.com``.
        headers: HTTP headers including authentication.
        ssl_verify: SSL verification setting (bool or CA bundle path).
        requests_module: Optional override for the ``requests`` library.
            When *None* (the default), ``requests`` is imported lazily at
            call time. Inject a mock here for unit testing.
    """

    base_url: str
    headers: dict[str, str]
    ssl_verify: bool | str = True
    requests_module: Any = field(default=None, repr=False, compare=False)


def _requests(config: JiraConfig) -> Any:
    """Return the requests module from *config*, falling back to a lazy import."""
    if config.requests_module is not None:
        return config.requests_module
    import requests  # pragma: no cover

    return requests  # pragma: no cover


# ---------------------------------------------------------------------------
# Result TypedDicts
# ---------------------------------------------------------------------------

EPIC_NAME_FIELD = "customfield_10006"


class CreateIssueResult(TypedDict):
    """Result of creating a Jira issue."""

    issue_key: str
    url: str
    raw_response: dict


class AddCommentResult(TypedDict):
    """Result of adding a comment to a Jira issue."""

    comment_id: str
    raw_response: dict


class FetchIssueContextResult(TypedDict):
    """Result of fetching Jira issue context."""

    issue: dict
    parent_issue: dict | None
    epic_issue: dict | None
    remote_links: list


# ---------------------------------------------------------------------------
# Tool functions
# ---------------------------------------------------------------------------


def create_issue(
    config: JiraConfig,
    project_key: str,
    summary: str,
    issue_type: str,
    description: str,
    labels: list[str],
    epic_name: str | None = None,
    parent_key: str | None = None,
) -> CreateIssueResult:
    """Create a Jira issue via the REST API.

    Args:
        config: Jira connection configuration.
        project_key: Jira project key (e.g. ``"PROJECT"``).
        summary: Issue summary / title.
        issue_type: Jira issue type name (``"Task"``, ``"Epic"``, ``"Sub-task"``, …).
        description: Issue description body.
        labels: Labels to apply.
        epic_name: Epic name field (required when *issue_type* is ``"Epic"``).
        parent_key: Parent issue key.  Required when *issue_type* resolves to a
            subtask type (i.e. ``issue_type.lower()`` is ``"sub-task"`` or
            ``"subtask"``); optional but accepted for any other issue type so
            that callers can set a parent on non-standard or localized issue
            types without additional Jira validation.

    Returns:
        A :class:`CreateIssueResult` with the new issue key, URL, and raw API
        response.

    Raises:
        ValueError: If *config.base_url* is empty, if *epic_name* is not
            provided when *issue_type* is ``"Epic"``, or if *parent_key* is not
            provided when *issue_type* is the literal string ``"Sub-task"`` or
            ``"subtask"`` (case-insensitive).
        requests.exceptions.HTTPError: On non-2xx API responses.
    """
    if not config.base_url:
        raise ValueError("base_url is required")

    if issue_type.lower() == "epic" and not epic_name:
        raise ValueError("epic_name is required when issue_type is 'Epic'")

    if issue_type.lower() in ("sub-task", "subtask") and not parent_key:
        raise ValueError("parent_key is required when issue_type is 'Sub-task'")

    requests = _requests(config)

    url = f"{config.base_url}/rest/api/2/issue"

    fields: dict[str, Any] = {
        "project": {"key": project_key},
        "summary": summary,
        "issuetype": {"name": issue_type},
        "description": description,
        "labels": labels,
    }

    if issue_type.lower() == "epic" and epic_name:
        fields[EPIC_NAME_FIELD] = epic_name

    if parent_key:
        fields["parent"] = {"key": parent_key}

    payload = {"fields": fields}

    response = requests.post(
        url,
        headers=config.headers,
        json=payload,
        verify=config.ssl_verify,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    issue_key = data.get("key") or ""

    if issue_key:
        browse_url = f"{config.base_url}/browse/{issue_key}"
    else:
        browse_url = ""

    return CreateIssueResult(
        issue_key=issue_key,
        url=browse_url,
        raw_response=data,
    )


def create_epic(
    config: JiraConfig,
    project_key: str,
    summary: str,
    epic_name: str,
    description: str,
    labels: list[str],
) -> CreateIssueResult:
    """Create a Jira Epic (convenience wrapper around :func:`create_issue`).

    Args:
        config: Jira connection configuration.
        project_key: Jira project key.
        summary: Epic summary / title.
        epic_name: The Epic Name field value.
        description: Epic description body.
        labels: Labels to apply.

    Returns:
        A :class:`CreateIssueResult`.
    """
    return create_issue(
        config=config,
        project_key=project_key,
        summary=summary,
        issue_type="Epic",
        description=description,
        labels=labels,
        epic_name=epic_name,
    )


def create_subtask(
    config: JiraConfig,
    project_key: str,
    summary: str,
    description: str,
    labels: list[str],
    parent_key: str,
    issue_type: str = "Sub-task",
) -> CreateIssueResult:
    """Create a Jira Sub-task (convenience wrapper around :func:`create_issue`).

    Args:
        config: Jira connection configuration.
        project_key: Jira project key.
        summary: Sub-task summary / title.
        description: Sub-task description body.
        labels: Labels to apply.
        parent_key: Parent issue key.
        issue_type: Sub-task issue type name. Must be a non-empty string.

    Returns:
        A :class:`CreateIssueResult`.

    Raises:
        ValueError: If *parent_key* or *issue_type* is blank.
    """
    if not isinstance(parent_key, str):
        raise ValueError("parent_key must be a string for subtask creation")
    normalized_parent_key = parent_key.strip()
    if not normalized_parent_key:
        raise ValueError("parent_key is required for subtask creation")
    if not isinstance(issue_type, str):
        raise ValueError("issue_type must be a string for subtask creation")
    normalized_issue_type = issue_type.strip()
    if not normalized_issue_type:
        raise ValueError("issue_type is required for subtask creation")
    return create_issue(
        config=config,
        project_key=project_key,
        summary=summary,
        issue_type=normalized_issue_type,
        description=description,
        labels=labels,
        parent_key=normalized_parent_key,
    )


def add_comment(
    config: JiraConfig,
    issue_key: str,
    comment: str,
) -> AddCommentResult:
    """Add a comment to an existing Jira issue.

    Args:
        config: Jira connection configuration.
        issue_key: The issue key to comment on (e.g. ``"PROJECT-1234"``).
        comment: Comment body text.

    Returns:
        An :class:`AddCommentResult` with the comment ID and raw response.

    Raises:
        ValueError: If *config.base_url* is empty.
        requests.exceptions.HTTPError: On non-2xx API responses.
    """
    if not config.base_url:
        raise ValueError("base_url is required")

    requests = _requests(config)

    url = f"{config.base_url}/rest/api/2/issue/{quote(issue_key, safe='')}/comment"
    payload = {"body": comment}

    response = requests.post(
        url,
        headers=config.headers,
        json=payload,
        verify=config.ssl_verify,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    return AddCommentResult(
        comment_id=str(data.get("id", "")),
        raw_response=data,
    )


def _fetch_remote_links(
    requests: Any,
    base_url: str,
    issue_key: str,
    headers: dict,
    ssl_verify: bool | str,
) -> list:
    """Fetch remote links (including PRs) for an issue."""
    url = f"{base_url}/rest/api/2/issue/{quote(issue_key, safe='')}/remotelink"
    try:
        response = requests.get(url, headers=headers, verify=ssl_verify, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result if isinstance(result, list) else []
    except Exception:
        return []


def _fetch_related_issue(
    requests: Any,
    base_url: str,
    issue_key: str,
    headers: dict,
    ssl_verify: bool | str,
) -> dict | None:
    """Fetch a related issue (parent or epic) by key."""
    fields = "summary,description,comment,labels,issuetype,parent,customfield_10008"
    url = f"{base_url}/rest/api/2/issue/{quote(issue_key, safe='')}?fields={fields}&comment.maxResults=50"
    try:
        response = requests.get(url, headers=headers, verify=ssl_verify, timeout=30)
        response.raise_for_status()
        related_issue = response.json()
        return related_issue if isinstance(related_issue, dict) else None
    except Exception:
        return None


def fetch_issue_context(
    config: JiraConfig,
    issue_key: str,
) -> FetchIssueContextResult:
    """Fetch full context for a Jira issue including parent and epic.

    Retrieves the issue details and, if applicable, its parent issue
    (for sub-tasks) and linked epic. Also fetches remote links.

    Args:
        config: Jira connection configuration.
        issue_key: The issue key to fetch (e.g. ``"PROJECT-1234"``).

    Returns:
        A :class:`FetchIssueContextResult` containing the issue, optional
        parent/epic, and remote links.

    Raises:
        ValueError: If *config.base_url* is empty.
        requests.exceptions.HTTPError: On non-2xx API responses for the
            main issue fetch (parent/epic/links failures are silenced).
    """
    if not config.base_url:
        raise ValueError("base_url is required")

    requests = _requests(config)

    fields_param = "*all"
    encoded_issue_key = quote(issue_key, safe="")
    # NOTE: Fetching *all fields for the main issue gives normalize() access to
    # status, dates, priority, components, and all customfield_* entries, but it
    # also increases the payload size and may surface sensitive data in logs/state.
    # Related issue fetches (_fetch_related_issue) still use a restrictive allowlist;
    # those should be widened separately if custom-field access is needed there too.
    url = f"{config.base_url}/rest/api/2/issue/{encoded_issue_key}?fields={fields_param}&comment.maxResults=50"

    response = requests.get(
        url,
        headers=config.headers,
        verify=config.ssl_verify,
        timeout=30,
    )
    response.raise_for_status()

    issue = response.json()
    # Guard against Jira returning a non-dict body (e.g. null or a list).
    if not isinstance(issue, dict):
        issue = {}

    # `fields` may be explicitly null in the response even when the key is
    # present — `.get("fields", {})` only substitutes the default when the key
    # is *missing*, not when the value is None, so we need an explicit isinstance
    # guard here (and for every nested dict we dereference below).
    fields = issue.get("fields")
    if not isinstance(fields, dict):
        fields = {}

    issuetype = fields.get("issuetype")
    if not isinstance(issuetype, dict):
        issuetype = {}
    is_subtask = bool(issuetype.get("subtask", False))
    issuetype_name = issuetype.get("name")
    is_epic = isinstance(issuetype_name, str) and issuetype_name.lower() == "epic"

    # Fetch parent issue for subtasks
    parent_issue: dict | None = None
    if is_subtask:
        parent_data = fields.get("parent")
        if not isinstance(parent_data, dict):
            parent_data = {}
        parent_key = parent_data.get("key")
        if parent_key:
            parent_issue = _fetch_related_issue(
                requests, config.base_url, parent_key, config.headers, config.ssl_verify
            )

    # Fetch epic (skip for subtasks and epics themselves)
    epic_issue: dict | None = None
    epic_link = fields.get("customfield_10008")
    if isinstance(epic_link, str) and epic_link and not is_subtask and not is_epic:
        epic_issue = _fetch_related_issue(requests, config.base_url, epic_link, config.headers, config.ssl_verify)

    # Fetch remote links
    remote_links = _fetch_remote_links(
        requests,
        config.base_url,
        issue_key,
        config.headers,
        config.ssl_verify,
    )

    return FetchIssueContextResult(
        issue=issue,
        parent_issue=parent_issue,
        epic_issue=epic_issue,
        remote_links=remote_links,
    )
