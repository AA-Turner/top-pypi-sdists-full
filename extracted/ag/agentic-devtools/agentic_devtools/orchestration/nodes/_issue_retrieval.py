"""Issue retrieval logic for Jira and GitHub providers.

Provides ``fetch_jira_issue_data`` and ``fetch_github_issue_data`` which
return a normalized 13-field issue data dictionary suitable for consumption
by downstream LangGraph nodes.
"""

from __future__ import annotations

import json
import logging
import re
import subprocess
from pathlib import Path
from typing import Any

from agentic_devtools.cli.jira.adf import _convert_adf_to_text

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Acceptance Criteria Extraction (FR-003)
# ---------------------------------------------------------------------------

# Maximum number of comments retained per issue (newest, chronological).
_MAX_COMMENTS = 30

_HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
# Jira wiki heading: h1. text  or  h3. +Decorated text+
_JIRA_HEADING_PATTERN = re.compile(r"^h([1-6])\.\s+(.+)$", re.MULTILINE)
# Strip Jira wiki inline markup such as +underline+ or *bold*
_JIRA_INLINE_MARKUP = re.compile(r"[+*_^~]")
_AUTH_ERROR_PATTERN = re.compile(r"\b(auth|authentication|unauthorized|forbidden|credentials?|token)\b", re.IGNORECASE)

_AC_HEADING_NAMES = (
    "acceptance criteria",
    "ac",
    "definition of done",
)


def _iter_headings(description: str) -> list[tuple[int, str, re.Match[str]]]:
    """Return (level, normalised_text, match) for every heading in *description*.

    Supports Markdown ATX headings (``# Heading``) and Jira wiki headings
    (``h3. +Heading+``), including wiki inline-markup decoration stripping.
    """
    result: list[tuple[int, str, re.Match[str]]] = []
    for m in _HEADING_PATTERN.finditer(description):
        level = len(m.group(1))
        text = m.group(2).strip().lower()
        result.append((level, text, m))
    for m in _JIRA_HEADING_PATTERN.finditer(description):
        level = int(m.group(1))
        raw_text = m.group(2).strip()
        text = _JIRA_INLINE_MARKUP.sub("", raw_text).strip().lower()
        result.append((level, text, m))
    # Stable sort by position in document
    result.sort(key=lambda t: t[2].start())
    return result


def extract_acceptance_criteria(description: str | None) -> str | None:
    """Extract acceptance criteria section from a description.

    Searches for headings matching (in priority order):
    "Acceptance Criteria", "AC", "Definition of Done".

    Supports Markdown ATX headings (``# Acceptance Criteria``) and Jira wiki
    headings (``h3. +Acceptance Criteria+``).

    Returns the content under the first matched heading until the next
    same-level-or-higher heading or end of text. Returns None if no
    matching heading is found.
    """
    if not description:
        return None

    headings = _iter_headings(description)
    if not headings:
        return None

    # Find the first matching heading by priority
    for target_name in _AC_HEADING_NAMES:
        for idx, (level, heading_text, match) in enumerate(headings):
            if heading_text == target_name:
                start = match.end()
                # Find end: next heading at same or higher level
                end = len(description)
                for other_level, _, other_match in headings[idx + 1 :]:
                    if other_level <= level:
                        end = other_match.start()
                        break
                content = description[start:end].strip()
                return content if content else None

    return None


# ---------------------------------------------------------------------------
# Jira Issue Retrieval (FR-001, FR-002)
# ---------------------------------------------------------------------------


def _build_jira_config() -> Any:
    """Construct a JiraConfig using existing CLI helpers.

    Raises:
        ValueError: If credentials or base URL cannot be resolved.
    """
    try:
        from agentic_devtools.cli.jira.config import get_jira_base_url, get_jira_headers
        from agentic_devtools.cli.jira.helpers import _get_requests, _get_ssl_verify
        from agentic_devtools.tools.jira import JiraConfig

        base_url = get_jira_base_url()
        headers = get_jira_headers()
        ssl_verify = _get_ssl_verify()
        requests_module = _get_requests()

        return JiraConfig(
            base_url=base_url,
            headers=headers,
            ssl_verify=ssl_verify,
            requests_module=requests_module,
        )
    except (ValueError, OSError, ImportError) as exc:
        raise ValueError(f"Failed to construct Jira configuration: {exc}") from exc


def _validate_jira_config(config: Any) -> None:
    """Validate that a JiraConfig has required credentials.

    Raises:
        ValueError: If base_url or Authorization header is missing.
    """
    if not hasattr(config, "base_url") or not isinstance(config.base_url, str):
        raise ValueError("Jira config is missing 'base_url' attribute — set JIRA_BASE_URL or configure in state")
    if not config.base_url:
        raise ValueError("Jira base_url is empty — set JIRA_BASE_URL or configure in state")
    if not hasattr(config, "headers"):
        raise ValueError("Jira config is missing 'headers' attribute — JIRA_COPILOT_PAT may not be set")
    auth = config.headers.get("Authorization", "") if isinstance(config.headers, dict) else ""
    if not auth:
        raise ValueError("Jira Authorization header is missing — set JIRA_COPILOT_PAT")


def _extract_http_status_code(exc: Exception) -> int | None:
    """Extract an HTTP status code from an exception when available."""
    status_code = getattr(exc, "status_code", None)
    if isinstance(status_code, int):
        return status_code

    response = getattr(exc, "response", None)
    response_status_code = getattr(response, "status_code", None)
    if isinstance(response_status_code, int):
        return response_status_code

    exc_str = str(exc)
    for pattern in (r"\bHTTP\s+(\d{3})\b", r"\bstatus(?:\s+code)?\s*[:=]?\s*(\d{3})\b"):
        match = re.search(pattern, exc_str, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None


def _looks_like_auth_error(exc: Exception) -> bool:
    """Return True when exception text indicates an authentication/authorization error."""
    return _AUTH_ERROR_PATTERN.search(str(exc)) is not None


def fetch_jira_issue_data(
    issue_key: str,
    *,
    config: Any | None = None,
    state_dir: Path | None = None,
) -> dict[str, Any]:
    """Fetch Jira issue details with parent/epic context.

    Args:
        issue_key: Jira issue key (e.g. ``PROJECT-1234``).
        config: Optional pre-built JiraConfig (for testing).
        state_dir: Optional state directory for persisting response files.

    Returns:
        Normalized 13-field issue data dictionary.

    Raises:
        ValueError: On credential/config failures.
        RuntimeError: On HTTP errors (401, 403, 404, etc.).
    """
    from agentic_devtools.tools.jira import fetch_issue_context

    if config is None:
        config = _build_jira_config()
    _validate_jira_config(config)

    try:
        ctx = fetch_issue_context(config, issue_key)
    except Exception as exc:
        status_code = _extract_http_status_code(exc)
        if status_code in {401, 403}:
            raise RuntimeError(
                f"Jira authentication failed for {issue_key}: {exc}. "
                "Verify the JIRA_COPILOT_PAT environment variable is set to a valid token."
            ) from exc
        if status_code == 404:
            raise RuntimeError(f"Jira issue not found: {issue_key}") from exc
        raise RuntimeError(f"Jira API error fetching {issue_key}: {exc}") from exc

    if not isinstance(ctx, dict) or "issue" not in ctx:
        raise RuntimeError(f"fetch_issue_context returned unexpected shape for {issue_key}: {type(ctx).__name__!r}")
    issue = ctx["issue"]
    # A malformed successful response (fetch_issue_context coerces a non-object
    # body to {}) must be treated as a retrieval error, not an empty issue.
    if not isinstance(issue, dict) or not issue:
        raise RuntimeError(f"Jira returned an empty or malformed issue payload for {issue_key}")
    parent_issue = ctx.get("parent_issue")
    epic_issue = ctx.get("epic_issue")

    # Persist raw responses
    if state_dir is not None:
        _persist_response(state_dir / "temp-get-issue-details-response.json", issue)
        if parent_issue is not None:
            _persist_response(state_dir / "temp-get-parent-issue-details-response.json", parent_issue)
        if epic_issue is not None:
            _persist_response(state_dir / "temp-get-epic-details-response.json", epic_issue)

    # Normalize
    fields = issue.get("fields") if isinstance(issue, dict) else None
    if not isinstance(fields, dict):
        fields = {}

    # Summary and description (handle ADF)
    raw_summary = fields.get("summary")
    summary = _convert_adf_to_text(raw_summary) if not isinstance(raw_summary, str) else raw_summary

    raw_description = fields.get("description")
    description = _convert_adf_to_text(raw_description) if not isinstance(raw_description, str) else raw_description

    # Issue type detection
    issuetype = fields.get("issuetype")
    if not isinstance(issuetype, dict):
        issuetype = {}
    issue_type_raw = issuetype.get("name", "")
    issue_type = issue_type_raw if isinstance(issue_type_raw, str) else ""
    is_subtask = bool(issuetype.get("subtask", False))

    # Status
    status_field = fields.get("status")
    status_raw = status_field.get("name", "") if isinstance(status_field, dict) else ""
    status = status_raw if isinstance(status_raw, str) else ""

    # Labels
    labels = fields.get("labels", [])
    if not isinstance(labels, list):
        labels = []

    # Comments (30 newest, chronological). The embedded issue payload only
    # returns the first page of comments (comment.maxResults=50, ordered
    # oldest-first), so when the issue has more comments than that page a
    # naive "last 30 of the page" would drop the actual newest comments.
    # Fetch the newest page directly in that case.
    comment_field = fields.get("comment")
    comments: list[dict[str, str]] = []
    if isinstance(comment_field, dict):
        raw_comments = comment_field.get("comments", [])
        raw_comments = raw_comments if isinstance(raw_comments, list) else []
        total = comment_field.get("total")
        if isinstance(total, int) and total > len(raw_comments):
            newest = _fetch_newest_jira_comments(config, issue_key, _MAX_COMMENTS)
            if newest is not None:
                raw_comments = newest
        # Filter to dict comments first, then sort/truncate so non-dict
        # entries don't consume slots and drop valid newest comments.
        dict_comments = [c for c in raw_comments if isinstance(c, dict)]
        dict_comments.sort(key=lambda c: str(c.get("created", "")))
        if len(dict_comments) > _MAX_COMMENTS:
            dict_comments = dict_comments[-_MAX_COMMENTS:]
        comments = [_normalize_jira_comment(c) for c in dict_comments]

    # Parent context
    parent_key: str | None = None
    parent_summary: str | None = None
    if is_subtask and parent_issue is not None:
        parent_fields = parent_issue.get("fields") if isinstance(parent_issue, dict) else None
        if isinstance(parent_fields, dict):
            parent_key = parent_issue.get("key")
            raw_parent_summary = parent_fields.get("summary")
            parent_summary = (
                _convert_adf_to_text(raw_parent_summary)
                if not isinstance(raw_parent_summary, str)
                else raw_parent_summary
            )
        else:
            parent_data = fields.get("parent")
            if isinstance(parent_data, dict):
                parent_key = parent_data.get("key")
    elif is_subtask:
        # Parent fetch may have failed but we can still get the key
        parent_data = fields.get("parent")
        if isinstance(parent_data, dict):
            parent_key = parent_data.get("key")

    # Epic context
    epic_key: str | None = None
    epic_summary: str | None = None
    issue_epic_link = fields.get("customfield_10008")
    if epic_issue is not None:
        epic_fields = epic_issue.get("fields") if isinstance(epic_issue, dict) else None
        if isinstance(epic_fields, dict):
            epic_key = epic_issue.get("key")
            raw_epic_summary = epic_fields.get("summary")
            epic_summary = (
                _convert_adf_to_text(raw_epic_summary) if not isinstance(raw_epic_summary, str) else raw_epic_summary
            )
    elif is_subtask and parent_issue is not None:
        # Try to get epic from parent's customfield_10008 and fetch its summary
        parent_fields_for_epic = parent_issue.get("fields") if isinstance(parent_issue, dict) else None
        if isinstance(parent_fields_for_epic, dict):
            epic_link = parent_fields_for_epic.get("customfield_10008")
            if isinstance(epic_link, str) and epic_link:
                epic_key = epic_link
                # Attempt to fetch epic details to get summary
                try:
                    epic_ctx = fetch_issue_context(config, epic_link)
                    fetched_epic = epic_ctx.get("issue")
                    if isinstance(fetched_epic, dict):
                        if state_dir is not None:
                            _persist_response(state_dir / "temp-get-epic-details-response.json", fetched_epic)
                        epic_fields = fetched_epic.get("fields")
                        if isinstance(epic_fields, dict):
                            raw_epic_summary = epic_fields.get("summary")
                            epic_summary = (
                                _convert_adf_to_text(raw_epic_summary)
                                if not isinstance(raw_epic_summary, str)
                                else raw_epic_summary
                            )
                except Exception as exc:  # noqa: BLE001
                    logger.warning("Failed to fetch epic %s for subtask %s: %s", epic_link, issue_key, exc)
    if epic_key is None and isinstance(issue_epic_link, str) and issue_epic_link:
        # fetch_issue_context() may suppress related epic lookup errors and return
        # epic_issue=None (or return a malformed epic payload); preserve the
        # explicit epic link from the primary issue so downstream planning keeps
        # the relationship even without summary text.
        epic_key = issue_epic_link
        logger.warning(
            "Jira epic context missing for %s; preserved epic link %s without summary",
            issue_key,
            issue_epic_link,
        )

    # Acceptance criteria
    acceptance_criteria = extract_acceptance_criteria(description)

    return {
        "key": issue_key,
        "provider": "jira",
        "summary": summary or "",
        "description": description or "",
        "status": status,
        "issue_type": issue_type,
        "labels": labels,
        "comments": comments,
        "parent_key": parent_key,
        "parent_summary": parent_summary,
        "epic_key": epic_key,
        "epic_summary": epic_summary,
        "acceptance_criteria": acceptance_criteria,
    }


# ---------------------------------------------------------------------------
# GitHub Issue Retrieval (FR-007)
# ---------------------------------------------------------------------------


def fetch_github_issue_data(
    issue_key: str,
    *,
    repo: str | None = None,
    state_dir: Path | None = None,
) -> dict[str, Any]:
    """Fetch GitHub issue details with comment truncation.

    Args:
        issue_key: Numeric issue ID or ``#``-prefixed form (e.g. ``42`` or ``#42``).
            The ``#`` prefix is stripped automatically before making the API call.
        repo: ``owner/repo`` string. Resolved from git remote if None.
        state_dir: Optional state directory for persisting the raw response file.

    Returns:
        Normalized 13-field issue data dictionary.

    Raises:
        RuntimeError: On gh CLI errors or repo resolution failures.
    """
    from agentic_devtools.adapters.github_adapter import GitHubIssuesAdapter
    from agentic_devtools.cli.github.repo_resolution import resolve_github_repo_safe
    from agentic_devtools.orchestration.nodes._helpers import normalize_github_issue_number

    normalized_key = normalize_github_issue_number(issue_key)
    if not normalized_key:
        raise RuntimeError("GitHub issue key must be a positive integer (e.g., '42' or '#42')")

    resolved_repo = repo or resolve_github_repo_safe()
    if not resolved_repo:
        raise RuntimeError("Cannot resolve GitHub repository from state or git remote")

    try:
        adapter = GitHubIssuesAdapter(repo=resolved_repo)
        issue_detail = adapter.get_issue(normalized_key)
    except FileNotFoundError as exc:
        raise RuntimeError("GitHub CLI is not installed or not on PATH") from exc
    except RuntimeError as exc:
        status_code = _extract_http_status_code(exc)
        exc_str = str(exc)
        if status_code == 404 or "not found" in exc_str.lower():
            raise RuntimeError(f"GitHub issue not found: {normalized_key}") from exc
        if status_code in {401, 403} or _looks_like_auth_error(exc):
            raise RuntimeError(f"GitHub authentication failed: {exc}") from exc
        raise RuntimeError(f"GitHub API error: {exc}") from exc

    if not isinstance(issue_detail, dict):
        raise RuntimeError(
            f"GitHub adapter returned unexpected type {type(issue_detail).__name__!r} for issue {normalized_key}"
        )

    # Persist raw response
    if state_dir is not None:
        _persist_response(state_dir / "temp-get-issue-details-response.json", issue_detail)

    # Extract and truncate comments (30 newest, chronological). Filter to dict
    # comments first so corrupted non-dict entries don't consume slots and drop
    # valid newest comments during truncation.
    #
    # gh issue view returns only one page of comments ordered oldest-first, so
    # for issues with more comments than that page can hold the embedded payload
    # omits the actual newest comments.  When the embedded list is at or above
    # the cap we fetch newest-first via the REST comments endpoint and fall back
    # to the embedded list on any failure.
    raw_comments = issue_detail.get("comments", [])
    comments: list[dict[str, str]] = []
    if isinstance(raw_comments, list):
        dict_comments: list[Any] = [c for c in raw_comments if isinstance(c, dict)]
        if len(dict_comments) >= _MAX_COMMENTS:
            newest = _fetch_newest_github_comments(resolved_repo, normalized_key, _MAX_COMMENTS)
            if newest is not None:
                dict_comments = newest
        dict_comments.sort(key=lambda c: c.get("created_at", ""))
        if len(dict_comments) > _MAX_COMMENTS:
            dict_comments = dict_comments[-_MAX_COMMENTS:]
        for c in dict_comments:
            comments.append(
                {
                    "comment_id": c.get("comment_id", ""),
                    "body": c.get("body", ""),
                    "created_at": c.get("created_at", ""),
                }
            )

    description_raw = issue_detail.get("description", "")
    description = description_raw if isinstance(description_raw, str) else ""
    acceptance_criteria = extract_acceptance_criteria(description)

    summary_raw = issue_detail.get("title", "")
    summary = summary_raw if isinstance(summary_raw, str) else ""
    status_raw = issue_detail.get("status", "")
    status = status_raw if isinstance(status_raw, str) else ""
    labels_raw = issue_detail.get("labels", [])
    labels: list[str] = labels_raw if isinstance(labels_raw, list) else []

    return {
        "key": normalized_key,
        "provider": "github",
        "summary": summary or "",
        "description": description,
        "status": status or "",
        "issue_type": None,
        "labels": labels,
        "comments": comments,
        "parent_key": None,
        "parent_summary": None,
        "epic_key": None,
        "epic_summary": None,
        "acceptance_criteria": acceptance_criteria,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalize_jira_comment(comment: dict[str, Any]) -> dict[str, str]:
    """Normalize a raw Jira comment dict into the stable 3-field shape.

    Non-string bodies (Jira Cloud ADF dict/list) are converted to plain text
    so downstream prompt content stays readable.
    """
    body_raw = comment.get("body", "")
    body = body_raw if isinstance(body_raw, str) else _convert_adf_to_text(body_raw)
    raw_id = comment.get("id")
    raw_created = comment.get("created")
    return {
        "comment_id": str(raw_id) if raw_id is not None else "",
        "body": body,
        "created_at": str(raw_created) if raw_created is not None else "",
    }


def _fetch_newest_jira_comments(config: Any, issue_key: str, limit: int) -> list[Any] | None:
    """Fetch the newest ``limit`` comments for a Jira issue (best-effort).

    Queries the dedicated comments endpoint ordered newest-first so truncation
    keeps the actual latest comments even when the issue has more comments than
    the embedded issue payload returns.

    Returns the raw ``comments`` list on success, or ``None`` on any failure so
    the caller falls back to the embedded (first-page) comments.
    """
    from urllib.parse import quote

    from agentic_devtools.tools.jira import _requests

    try:
        requests = _requests(config)
        encoded_key = quote(issue_key, safe="")
        url = f"{config.base_url}/rest/api/2/issue/{encoded_key}/comment?orderBy=-created&maxResults={limit}"
        response = requests.get(url, headers=config.headers, verify=config.ssl_verify, timeout=30)
        response.raise_for_status()
        payload = response.json()
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to fetch newest comments for %s: %s", issue_key, exc)
        return None

    if not isinstance(payload, dict):
        return None
    raw = payload.get("comments")
    return raw if isinstance(raw, list) else None


def _fetch_newest_github_comments(repo: str, issue_number: str, limit: int) -> list[dict[str, str]] | None:
    """Fetch the newest ``limit`` comments for a GitHub issue (best-effort).

    The GitHub REST comments endpoint does not support ``direction``; it only
    supports pagination and ``since``.  This function paginates through all
    pages (100 comments per page) and returns the last ``limit`` entries so
    that truncation keeps the actual newest comments even when the issue has
    more than one page of comments.

    Each returned dict uses the same 3-field shape as
    :class:`~agentic_devtools.adapters.types.Comment` (``comment_id``,
    ``body``, ``created_at``) so the caller can sort and slice without further
    normalization.

    Returns the normalized comment list on success, or ``None`` on any failure
    so the caller falls back to the embedded (first-page) comments.
    """
    from agentic_devtools.cli.subprocess_utils import run_safe

    _PER_PAGE = 100
    all_entries: list[dict] = []
    page = 1
    while True:
        try:
            result: subprocess.CompletedProcess = run_safe(
                [
                    "gh",
                    "api",
                    f"repos/{repo}/issues/{issue_number}/comments?per_page={_PER_PAGE}&page={page}",
                ],
                capture_output=True,
                text=True,
                shell=False,
            )
            if result.returncode != 0:
                logger.warning(
                    "Failed to fetch newest GitHub comments for %s#%s (page %d): %s",
                    repo,
                    issue_number,
                    page,
                    result.stderr,
                )
                return None
            page_list = json.loads(result.stdout)
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Failed to fetch newest GitHub comments for %s#%s (page %d): %s",
                repo,
                issue_number,
                page,
                exc,
            )
            return None

        if not isinstance(page_list, list):
            return None
        all_entries.extend(e for e in page_list if isinstance(e, dict))
        if len(page_list) < _PER_PAGE:
            break
        page += 1

    # Keep only the newest `limit` entries (the list is already oldest-first).
    newest = all_entries[-limit:] if len(all_entries) > limit else all_entries
    normalized: list[dict[str, str]] = []
    for entry in newest:
        raw_id = entry.get("id")
        raw_body = entry.get("body")
        raw_created = entry.get("created_at")
        normalized.append(
            {
                "comment_id": str(raw_id) if raw_id is not None else "",
                "body": raw_body if isinstance(raw_body, str) else "",
                "created_at": raw_created if isinstance(raw_created, str) else "",
            }
        )
    return normalized


def _persist_response(path: Path, data: Any) -> None:
    """Persist raw API response to JSON file (best-effort)."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    except OSError as exc:
        logger.warning("Failed to persist response to %s: %s", path, exc)
