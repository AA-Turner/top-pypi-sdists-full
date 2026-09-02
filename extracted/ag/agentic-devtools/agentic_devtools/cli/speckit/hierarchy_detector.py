"""GitHub sub-issues hierarchy detector for SpecKit nested spec management.

Provides ``GitHubHierarchyDetector``, a concrete implementation of the
``HierarchyDetector`` protocol that queries GitHub's sub-issues API to discover
parent/child relationships, determine hierarchy levels, and return structured
``HierarchyNode`` data.

Uses the ``gh`` CLI via ``run_safe()`` for all API calls (REST and GraphQL).
"""

from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from typing import Any

from agentic_devtools.cli.speckit.hierarchy import (
    ChildEntry,
    HierarchyDetector,
    HierarchyLevel,
    HierarchyNode,
    HierarchyValidationError,
)
from agentic_devtools.cli.subprocess_utils import run_safe

__all__ = [
    "GitHubHierarchyDetector",
    "JiraHierarchyDetector",
    "get_hierarchy_detector",
    "parse_issue_reference",
]

# Maximum retry attempts for API calls with exponential backoff
_MAX_RETRIES = 5
# Initial backoff duration in seconds
_INITIAL_BACKOFF = 1.0
# Maximum backoff cap in seconds
_MAX_BACKOFF = 60.0
# Maximum hierarchy depth (Epic -> Feature -> Task)
_MAX_DEPTH = 3
# Maximum sub-issues returned per GraphQL page
_GRAPHQL_SUB_ISSUES_PAGE_SIZE = 100
# Maximum number of child issues checked in a single batch GraphQL query
_GRAPHQL_SUB_ISSUES_BATCH_SIZE = 50
_STRUCTURED_HTTP_403_RE = re.compile(r"(?im)\b(?:http|status)\s+403\b|^\s*403\b")


def _has_structured_http_403(stderr: str | None) -> bool:
    """Return True only for stderr that names HTTP status 403 in context.

    Matches structured forms such as ``HTTP 403``, ``status 403``, or a bare
    ``403`` at the start of a line. This intentionally does **not** match issue
    identifiers embedded in URLs like ``.../issues/403``.
    """
    if stderr is None:
        return False
    return bool(_STRUCTURED_HTTP_403_RE.search(stderr))


def parse_issue_reference(
    issue_key: str | int,
    default_owner: str,
    default_repo: str,
) -> tuple[str, str, int]:
    """Parse an issue reference into (owner, repo, issue_number).

    Supported formats:
        - Bare number: ``"42"`` → ``(default_owner, default_repo, 42)``
        - Hash-prefixed: ``"#42"`` → ``(default_owner, default_repo, 42)``
        - Qualified: ``"owner/repo#42"`` → ``("owner", "repo", 42)``

    Args:
        issue_key: Issue identifier in any supported format.
        default_owner: Owner to use for bare/hash-prefixed references.
        default_repo: Repo to use for bare/hash-prefixed references.

    Returns:
        Tuple of (owner, repo, issue_number).

    Raises:
        ValueError: If the issue_key format is not recognized or the issue
            number is not a positive integer (>= 1).
    """
    issue_key = str(issue_key).strip()

    # Bare number: "42"
    if issue_key.isdigit():
        number = int(issue_key)
        if number < 1:
            raise ValueError(f"Invalid issue number: {number!r}. GitHub issue numbers must be >= 1.")
        return (default_owner, default_repo, number)

    # Hash-prefixed: "#42"
    if issue_key.startswith("#") and issue_key[1:].isdigit():
        number = int(issue_key[1:])
        if number < 1:
            raise ValueError(f"Invalid issue number: {number!r}. GitHub issue numbers must be >= 1.")
        return (default_owner, default_repo, number)

    # Qualified: "owner/repo#42" — neither owner nor repo segments may contain '/' or '#'
    qualified_match = re.fullmatch(r"([^/#]+)/([^/#]+)#(\d+)", issue_key)
    if qualified_match:
        owner = qualified_match.group(1)
        repo = qualified_match.group(2)
        number = int(qualified_match.group(3))
        if number < 1:
            raise ValueError(f"Invalid issue number: {number!r}. GitHub issue numbers must be >= 1.")
        return (owner, repo, number)

    raise ValueError(
        f"Invalid issue reference format: {issue_key!r}. "
        "Expected bare number ('42'), hash-prefixed ('#42'), "
        "or qualified ('owner/repo#42')."
    )


def _split_header_body_blocks(raw_output: str) -> list[tuple[str, str]]:
    """Split ``gh api --include`` output into (headers, body) pairs.

    When ``--include`` and ``--paginate`` are both used, ``gh`` prepends HTTP
    header blocks before each page's JSON body. This function splits on
    ``HTTP/`` boundaries and pairs each header block with the following body.
    """
    # Split on lines starting with HTTP/ (the response status line)
    parts = re.split(r"(?m)^(HTTP/\S+ \d+[^\n]*\n)", raw_output)

    blocks: list[tuple[str, str]] = []
    i = 1  # Skip any leading content before the first HTTP/ line
    while i < len(parts):
        status_line = parts[i]
        # The headers are status line + everything until the body
        remaining = parts[i + 1] if i + 1 < len(parts) else ""
        # Headers end at the first empty line (double newline)
        header_body_split = re.split(r"\n\n|\r\n\r\n", remaining, maxsplit=1)
        if len(header_body_split) == 2:
            headers = status_line + header_body_split[0]
            body = header_body_split[1]
        else:
            headers = status_line + remaining
            body = ""
        blocks.append((headers, body))
        i += 2

    return blocks


def _parse_rate_limit_headers(headers: str) -> tuple[int, float]:
    """Extract rate-limit info from HTTP response headers.

    Args:
        headers: Raw HTTP headers string.

    Returns:
        Tuple of (remaining_requests, reset_timestamp).
        Defaults to (9999, 0.0) if headers are missing/unparseable.
    """
    remaining = 9999
    reset_ts = 0.0

    remaining_match = re.search(r"(?i)x-ratelimit-remaining:\s*(\d+)", headers)
    if remaining_match:
        remaining = int(remaining_match.group(1))

    reset_match = re.search(r"(?i)x-ratelimit-reset:\s*(\d+)", headers)
    if reset_match:
        reset_ts = float(reset_match.group(1))

    return (remaining, reset_ts)


def _normalize_issue_title(raw_title: Any, issue_number: Any) -> str:
    """Normalize issue title values to a non-empty display string."""
    if isinstance(raw_title, str):
        normalized = raw_title.strip()
        if normalized:
            return normalized
    return f"Issue #{issue_number}"


def _raise_for_graphql_errors(data: Any) -> None:
    """Raise on GraphQL responses that contain an ``errors`` payload."""
    if not isinstance(data, dict):
        return

    errors = data.get("errors")
    if not isinstance(errors, list) or not errors:
        return

    messages = []
    for error in errors:
        if isinstance(error, dict) and isinstance(error.get("message"), str):
            messages.append(error["message"])
        else:
            messages.append(str(error))

    raise HierarchyValidationError(
        "api",
        "GitHub GraphQL API returned errors: " + "; ".join(messages),
    )


class GitHubHierarchyDetector:
    """Concrete implementation of HierarchyDetector for GitHub sub-issues.

    Uses the ``gh`` CLI to query GitHub REST and GraphQL APIs for
    parent/child relationships and hierarchy classification.

    Args:
        owner: GitHub repository owner (organization or user).
        repo: GitHub repository name.
        rate_limit_threshold: Pause requests when remaining quota drops below
            this value. Default: 10.
    """

    def __init__(self, owner: str, repo: str, *, rate_limit_threshold: int = 10) -> None:
        self.owner = owner
        self.repo = repo
        self.rate_limit_threshold = rate_limit_threshold
        self._rate_limit_remaining: int = 9999
        self._rate_limit_reset: float = 0.0

    def _check_rate_limit(self) -> None:
        """Proactively pause if rate limit is approaching threshold."""
        if self._rate_limit_remaining < self.rate_limit_threshold:
            pause_duration = max(1.0, min(self._rate_limit_reset - time.time(), 120.0))
            time.sleep(pause_duration)

    def _update_rate_limit(self, headers: str) -> None:
        """Update internal rate-limit state from response headers."""
        remaining, reset_ts = _parse_rate_limit_headers(headers)
        self._rate_limit_remaining = remaining
        self._rate_limit_reset = reset_ts

    def _run_gh_rest(
        self,
        endpoint: str,
        *,
        paginate: bool = True,
    ) -> tuple[Any, str]:
        """Execute a GitHub REST API call via ``gh api``.

        Args:
            endpoint: API endpoint path (e.g., ``repos/owner/repo/issues/42/sub_issues``).
            paginate: Whether to use ``--paginate`` flag.

        Returns:
            Tuple of (parsed_json_data, last_page_headers_string).

        Raises:
            HierarchyValidationError: On non-recoverable API errors.
        """
        self._check_rate_limit()

        cmd = ["gh", "api", endpoint, "--include"]
        if paginate:
            cmd.append("--paginate")

        backoff = _INITIAL_BACKOFF
        last_error: str | None = None

        for attempt in range(_MAX_RETRIES):
            last_error = None  # Reset per attempt; stale errors must not short-circuit a subsequent successful parse
            try:
                result = run_safe(cmd, capture_output=True, text=True, shell=False)
            except FileNotFoundError as exc:
                raise HierarchyValidationError(
                    "api",
                    "GitHub CLI (`gh`) is not installed or not available in PATH",
                ) from exc

            if result.returncode == 0 and result.stdout.strip():
                # Parse the response
                blocks = _split_header_body_blocks(result.stdout)
                if not blocks:
                    # Fallback: try parsing entire stdout as JSON
                    try:
                        data = json.loads(result.stdout)
                        return (data, "")
                    except json.JSONDecodeError:
                        last_error = "Empty or unparseable response"
                        if attempt < _MAX_RETRIES - 1:
                            time.sleep(backoff)
                            backoff = min(backoff * 2, _MAX_BACKOFF)
                        continue

                # Merge JSON bodies from all pages
                merged_data: list[Any] = []
                last_headers = ""
                parsed_any_body = False
                for headers, body in blocks:
                    last_headers = headers
                    body = body.strip()
                    if body:
                        try:
                            parsed = json.loads(body)
                            if isinstance(parsed, list):
                                merged_data.extend(parsed)
                                parsed_any_body = True
                            else:
                                # Single object response (non-paginated)
                                self._update_rate_limit(last_headers)
                                return (parsed, last_headers)
                        except json.JSONDecodeError:
                            last_error = f"Malformed JSON in API response: {body[:100]}"
                            break

                # If blocks were present but no JSON body was parsed in any of them
                # (all pages had headers-only or whitespace-only bodies), treat this
                # as a retryable error rather than silently returning an empty list.
                if not parsed_any_body and not last_error:
                    last_error = "Headers-only response: no JSON body found in any page"

                if last_error:
                    if attempt < _MAX_RETRIES - 1:
                        time.sleep(backoff)
                        backoff = min(backoff * 2, _MAX_BACKOFF)
                    continue

                self._update_rate_limit(last_headers)
                return (merged_data, last_headers)

            # Check for 404 - fail fast, no retry. Preserve stderr context so
            # callers can distinguish repo-wide failures from per-issue 404s.
            if "404" in (result.stderr or "") or "Not Found" in (result.stderr or ""):
                raise HierarchyValidationError(
                    "api",
                    f"GitHub REST API returned HTTP 404 for {endpoint}: {(result.stderr or '').strip()}",
                )

            # Check for 403 - rate-limit 403 retries via rate-limit helpers;
            # non-rate-limit 403 (bad auth / insufficient scope) fails fast.
            # Require structured HTTP/status context so issue URLs like
            # /issues/403 are not misclassified as auth failures.
            if _has_structured_http_403(result.stderr):
                stderr_lower = (result.stderr or "").lower()
                if "rate limit" in stderr_lower:
                    # Rate-limit 403: update state and retry with backoff
                    self._update_rate_limit(result.stdout or "")
                    self._check_rate_limit()
                    last_error = result.stderr
                    if attempt < _MAX_RETRIES - 1:
                        time.sleep(backoff)
                        backoff = min(backoff * 2, _MAX_BACKOFF)
                    continue
                raise HierarchyValidationError(
                    "api",
                    f"GitHub REST API returned HTTP 403 (insufficient token scope or invalid auth): {result.stderr}",
                )

            # Retryable error - apply backoff
            if result.returncode == 0:
                last_error = "gh api returned an empty response"
            else:
                last_error = result.stderr or f"gh api failed with exit code {result.returncode}"
            if attempt < _MAX_RETRIES - 1:
                time.sleep(backoff)
                backoff = min(backoff * 2, _MAX_BACKOFF)

        raise HierarchyValidationError(
            "api",
            f"GitHub REST API failed after {_MAX_RETRIES} attempts: {last_error}",
        )

    def _check_graphql_errors_retryable(
        self,
        data: Any,
        attempt: int,
        backoff: float,
    ) -> tuple[str | None, float]:
        """Check for GraphQL errors in a parsed response and apply backoff if retryable.

        Args:
            data: Parsed JSON response dict.
            attempt: Current attempt index (0-based).
            backoff: Current backoff duration in seconds.

        Returns:
            ``(None, backoff)`` when no errors are present (caller should proceed normally).
            ``(error_message, updated_backoff)`` when GraphQL errors are found (caller should
            update ``last_error`` and ``continue`` the retry loop).
        """
        try:
            _raise_for_graphql_errors(data)
            return (None, backoff)
        except HierarchyValidationError as gql_err:
            if attempt < _MAX_RETRIES - 1:
                time.sleep(backoff)
                backoff = min(backoff * 2, _MAX_BACKOFF)
            return (str(gql_err), backoff)

    def _run_gh_graphql(
        self,
        query: str,
        variables: dict[str, Any],
    ) -> tuple[dict[str, Any], str]:
        """Execute a GitHub GraphQL API call via ``gh api graphql``.

        Args:
            query: GraphQL query string.
            variables: Query variables as key-value pairs.

        Returns:
            Tuple of (parsed_json_response, headers_string).

        Raises:
            HierarchyValidationError: On non-recoverable API errors.
        """
        self._check_rate_limit()

        cmd = ["gh", "api", "graphql", "--include"]
        cmd.extend(["--raw-field", f"query={query}"])
        for key, value in variables.items():
            if isinstance(value, str):
                cmd.extend(["--raw-field", f"{key}={value}"])
            else:
                cmd.extend(["--field", f"{key}={value}"])

        backoff = _INITIAL_BACKOFF
        last_error: str | None = None

        for attempt in range(_MAX_RETRIES):
            try:
                result = run_safe(cmd, capture_output=True, text=True, shell=False)
            except FileNotFoundError as exc:
                raise HierarchyValidationError(
                    "api",
                    "GitHub CLI (`gh`) is not installed or not available in PATH",
                ) from exc

            if result.returncode == 0 and result.stdout.strip():
                # Parse headers + body
                last_headers = ""
                blocks = _split_header_body_blocks(result.stdout)
                if blocks:
                    last_headers = blocks[-1][0]
                    body = blocks[-1][1].strip()
                    if body:
                        try:
                            data = json.loads(body)
                            self._update_rate_limit(last_headers)
                            gql_err_msg, backoff = self._check_graphql_errors_retryable(data, attempt, backoff)
                            if gql_err_msg is not None:
                                last_error = gql_err_msg
                                continue
                            return (data, last_headers)
                        except json.JSONDecodeError:
                            last_error = f"Malformed JSON in GraphQL response: {body[:100]}"
                            if attempt < _MAX_RETRIES - 1:
                                time.sleep(backoff)
                                backoff = min(backoff * 2, _MAX_BACKOFF)
                            continue

                # Fallback: try parsing stdout directly (no --include headers)
                try:
                    # Try to find JSON in the raw output
                    raw = result.stdout.strip()
                    # Skip headers if present
                    json_start = raw.find("{")
                    if json_start >= 0:
                        data = json.loads(raw[json_start:])
                        if last_headers:
                            self._update_rate_limit(last_headers)
                        gql_err_msg, backoff = self._check_graphql_errors_retryable(data, attempt, backoff)
                        if gql_err_msg is not None:
                            last_error = gql_err_msg
                            continue
                        return (data, last_headers)
                except json.JSONDecodeError:
                    pass

                last_error = "Empty or unparseable GraphQL response"
                if attempt < _MAX_RETRIES - 1:
                    time.sleep(backoff)
                    backoff = min(backoff * 2, _MAX_BACKOFF)
                continue

            # Check for 403 - rate-limit 403 retries via rate-limit helpers;
            # non-rate-limit 403 (bad auth / insufficient scope) fails fast.
            # Require structured HTTP/status context so issue URLs like
            # /issues/403 are not misclassified as auth failures.
            if _has_structured_http_403(result.stderr):
                stderr_lower = (result.stderr or "").lower()
                if "rate limit" in stderr_lower:
                    # Rate-limit 403: update state and retry with backoff
                    self._update_rate_limit(result.stdout or "")
                    self._check_rate_limit()
                    last_error = result.stderr
                    if attempt < _MAX_RETRIES - 1:
                        time.sleep(backoff)
                        backoff = min(backoff * 2, _MAX_BACKOFF)
                    continue
                raise HierarchyValidationError(
                    "api",
                    f"GitHub GraphQL API returned HTTP 403 (insufficient token scope or invalid auth): {result.stderr}",
                )

            # Retryable error - apply backoff
            if result.returncode == 0:
                last_error = "gh api graphql returned an empty response"
            else:
                last_error = result.stderr or f"gh api graphql failed with exit code {result.returncode}"
            if attempt < _MAX_RETRIES - 1:
                time.sleep(backoff)
                backoff = min(backoff * 2, _MAX_BACKOFF)

        raise HierarchyValidationError(
            "api",
            f"GitHub GraphQL API failed after {_MAX_RETRIES} attempts: {last_error}",
        )

    def _fetch_issue_title(self, owner: str, repo: str, issue_number: int) -> str:
        """Fetch the title of a single issue via REST API.

        Args:
            owner: Repository owner.
            repo: Repository name.
            issue_number: Issue number.

        Returns:
            Issue title string.

        Raises:
            HierarchyValidationError: If the issue cannot be found or API fails.
        """
        endpoint = f"repos/{owner}/{repo}/issues/{issue_number}"
        data, _headers = self._run_gh_rest(endpoint, paginate=False)
        if isinstance(data, dict) and "title" in data:
            return _normalize_issue_title(data["title"], issue_number)
        raise HierarchyValidationError(
            "title",
            f"Could not retrieve title for {owner}/{repo}#{issue_number}",
        )

    def validate_repository_access(self) -> None:
        """Verify that the configured repository is accessible via the GitHub API.

        Performs a lightweight ``GET /repos/{owner}/{repo}`` call.  Raises
        immediately on permission errors (403), missing repositories (404), and
        other non-recoverable failures so callers can fail fast rather than
        discovering the misconfiguration through per-issue 404 warnings.

        Raises:
            HierarchyValidationError: If the repository cannot be accessed.
        """
        endpoint = f"repos/{self.owner}/{self.repo}"
        try:
            self._run_gh_rest(endpoint, paginate=False)
        except HierarchyValidationError as exc:
            raise HierarchyValidationError(
                "api",
                f"Repository '{self.owner}/{self.repo}' is inaccessible or does not exist. "
                f"Verify the repository name and GitHub authentication. ({exc.detail})",
            ) from exc

    def get_children(self, owner: str, repo: str, issue_number: int) -> list[ChildEntry]:
        """Get ordered list of child issues (sub-issues) for a given issue.

        Uses REST API as primary source, falls back to GraphQL on failure.

        Args:
            owner: Repository owner.
            repo: Repository name.
            issue_number: Parent issue number.

        Returns:
            Ordered list of ChildEntry instances. Empty list if no sub-issues.
        """
        try:
            return self._get_children_rest(owner, repo, issue_number)
        except HierarchyValidationError as exc:
            # 404 means issue not found - don't fallback
            if "404" in str(exc):
                raise
            # Other errors: try GraphQL fallback
            print(
                f"Warning: REST sub-issues endpoint failed for {owner}/{repo}#{issue_number}, "
                f"falling back to GraphQL: {exc}",
                file=sys.stderr,
            )
            return self._get_children_graphql(owner, repo, issue_number)

    def _get_children_rest(self, owner: str, repo: str, issue_number: int) -> list[ChildEntry]:
        """Fetch children via REST sub_issues endpoint."""
        endpoint = f"repos/{owner}/{repo}/issues/{issue_number}/sub_issues"
        data, _headers = self._run_gh_rest(endpoint)

        if not isinstance(data, list):
            return []

        children: list[ChildEntry] = []
        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                continue

            child_number = item.get("number")
            if child_number is None:
                continue

            title = _normalize_issue_title(item.get("title"), child_number)

            # Assign 1-based order by position in response list (FR-007)
            order_value = idx + 1

            # Check for cross-repo children
            child_repo_info = item.get("repository")
            if isinstance(child_repo_info, dict):
                raw_owner = child_repo_info.get("owner")
                child_owner = raw_owner.get("login", owner) if isinstance(raw_owner, dict) else owner
                raw_name = child_repo_info.get("name")
                child_repo_name = raw_name if isinstance(raw_name, str) else repo
                if child_owner != owner or child_repo_name != repo:
                    # Cross-repo child - use qualified key
                    key = f"{child_owner}/{child_repo_name}#{child_number}"
                    print(
                        f"Warning: Cross-repo child reference {key} for {owner}/{repo}#{issue_number}",
                        file=sys.stderr,
                    )
                    children.append(ChildEntry(key=key, title=title, order=order_value))
                    continue

            children.append(ChildEntry(key=str(child_number), title=title, order=order_value))

        return children

    def _get_children_graphql(self, owner: str, repo: str, issue_number: int) -> list[ChildEntry]:
        """Fetch children via GraphQL subIssues query (fallback)."""
        query = (
            "query($owner: String!, $repo: String!, $number: Int!) {"
            "  repository(owner: $owner, name: $repo) {"
            "    issue(number: $number) {"
            f"      subIssues(first: {_GRAPHQL_SUB_ISSUES_PAGE_SIZE}) {{"
            "        pageInfo { hasNextPage }"
            "        nodes { number title }"
            "      }"
            "    }"
            "  }"
            "}"
        )
        variables = {"owner": owner, "repo": repo, "number": issue_number}

        data, _headers = self._run_gh_graphql(query, variables)

        response_data = data.get("data")
        repository_data = response_data.get("repository") if isinstance(response_data, dict) else None
        if not isinstance(repository_data, dict):
            raise HierarchyValidationError(
                "api",
                f"GitHub GraphQL response missing repository for {owner}/{repo}",
            )
        issue_data = repository_data.get("issue")
        if not isinstance(issue_data, dict):
            raise HierarchyValidationError(
                "api",
                f"GitHub GraphQL response missing issue {owner}/{repo}#{issue_number}",
            )
        sub_issues_data = issue_data.get("subIssues")
        nodes = sub_issues_data.get("nodes") if isinstance(sub_issues_data, dict) else []
        if not isinstance(nodes, list):
            nodes = []

        # Warn only when there is confirmed evidence of more pages;
        # default has_next to False so missing/malformed pageInfo never triggers a false positive.
        if len(nodes) >= _GRAPHQL_SUB_ISSUES_PAGE_SIZE:
            page_info = sub_issues_data.get("pageInfo") if isinstance(sub_issues_data, dict) else None
            has_next = page_info.get("hasNextPage") if isinstance(page_info, dict) else False
            if has_next:
                print(
                    f"Warning: {owner}/{repo}#{issue_number} has more than "
                    f"{_GRAPHQL_SUB_ISSUES_PAGE_SIZE} sub-issues; the GraphQL fallback returned "
                    "only the first page and the hierarchy may be incomplete.",
                    file=sys.stderr,
                )

        children: list[ChildEntry] = []
        for idx, node in enumerate(nodes):
            if not isinstance(node, dict):
                continue
            number = node.get("number")
            if number is None:
                continue
            title = _normalize_issue_title(node.get("title"), number)
            children.append(ChildEntry(key=str(number), title=title, order=idx + 1))

        return children

    def get_parent(self, owner: str, repo: str, issue_number: int) -> str | None:
        """Get the parent issue number for a given issue.

        Uses GraphQL API (parent field is not available via REST).

        Args:
            owner: Repository owner.
            repo: Repository name.
            issue_number: Issue number to check.

        Returns:
            Parent issue number as string, or None if no parent.
        """
        query = (
            "query($owner: String!, $repo: String!, $number: Int!) {"
            "  repository(owner: $owner, name: $repo) {"
            "    issue(number: $number) {"
            "      parent { number }"
            "    }"
            "  }"
            "}"
        )
        variables = {"owner": owner, "repo": repo, "number": issue_number}

        data, _headers = self._run_gh_graphql(query, variables)

        response_data = data.get("data")
        repository_data = response_data.get("repository") if isinstance(response_data, dict) else None
        if not isinstance(repository_data, dict):
            raise HierarchyValidationError(
                "api",
                f"GitHub GraphQL response missing repository for {owner}/{repo}",
            )
        issue_data = repository_data.get("issue")
        if not isinstance(issue_data, dict):
            raise HierarchyValidationError(
                "api",
                f"GitHub GraphQL response missing issue {owner}/{repo}#{issue_number}",
            )

        parent_data = issue_data.get("parent")
        if parent_data is None or not isinstance(parent_data, dict):
            return None

        parent_number = parent_data.get("number")
        if parent_number is None:
            return None

        return str(parent_number)

    def _build_batch_subissues_query(self, child_numbers: list[int]) -> str:
        """Build aliased GraphQL query to check if children have sub-issues.

        Args:
            child_numbers: List of child issue numbers to check.

        Returns:
            GraphQL query string with aliased fields per child.
        """
        aliases = []
        for num in child_numbers:
            aliases.append(f"    issue_{num}: issue(number: {num}) {{ subIssues(first: 1) {{ totalCount }} }}")
        alias_str = "\n".join(aliases)
        return (
            "query($owner: String!, $repo: String!) {\n"
            "  repository(owner: $owner, name: $repo) {\n"
            f"{alias_str}\n"
            "  }\n"
            "}"
        )

    def _batch_check_children_have_children(self, owner: str, repo: str, child_numbers: list[int]) -> dict[int, bool]:
        """Check which children have their own sub-issues via batched GraphQL.

        Args:
            owner: Repository owner.
            repo: Repository name.
            child_numbers: Issue numbers to check.

        Returns:
            Dict mapping issue_number -> has_children (bool).
        """
        if not child_numbers:
            return {}

        result: dict[int, bool] = {}

        for start in range(0, len(child_numbers), _GRAPHQL_SUB_ISSUES_BATCH_SIZE):
            child_batch = child_numbers[start : start + _GRAPHQL_SUB_ISSUES_BATCH_SIZE]
            query = self._build_batch_subissues_query(child_batch)
            variables = {"owner": owner, "repo": repo}

            data, _headers = self._run_gh_graphql(query, variables)

            response_data = data.get("data")
            repo_data = response_data.get("repository") if isinstance(response_data, dict) else None
            if not isinstance(repo_data, dict):
                raise HierarchyValidationError(
                    "api",
                    f"GitHub GraphQL response missing repository for {owner}/{repo}",
                )

            for num in child_batch:
                alias = f"issue_{num}"
                raw_issue = repo_data.get(alias)
                issue_data = raw_issue if isinstance(raw_issue, dict) else {}
                raw_sub_issues = issue_data.get("subIssues")
                sub_issues = raw_sub_issues if isinstance(raw_sub_issues, dict) else {}
                total_count = sub_issues.get("totalCount", 0)
                result[num] = total_count > 0 if isinstance(total_count, int) else False

        return result

    def get_level(
        self,
        owner: str,
        repo: str,
        issue_number: int,
        *,
        _depth: int = 0,
    ) -> HierarchyLevel:
        """Classify an issue's hierarchy level.

        Classification rules (primary — children-based):
            - Has children, at least one child has children → EPIC
            - Has children, none have children → FEATURE
            - Batch query failure → FEATURE (conservative) + warning

        Classification rules (secondary — depth-based, when no children):
            - No children, depth 1 from root → FEATURE
            - No children, depth >= 2 → TASK
            - No children, no parent (standalone) → TASK
            - depth >= MAX_DEPTH (cap) → TASK with warning

        Args:
            owner: Repository owner.
            repo: Repository name.
            issue_number: Issue number to classify.
            _depth: Internal depth counter (do not pass externally).

        Returns:
            HierarchyLevel classification.
        """
        children = self.get_children(owner, repo, issue_number)
        # Parent is needed for depth-cap enforcement. When _depth is inferred
        # (_depth == 0), fetch parent even for non-leaf nodes so deep hierarchies
        # short-circuit to TASK before child-shape classification.
        parent = self.get_parent(owner, repo, issue_number) if (_depth == 0 or not children) else None
        return self._classify_level(owner, repo, issue_number, children, parent, _depth)

    def _infer_leaf_depth(
        self,
        owner: str,
        repo: str,
        issue_number: int,
        parent: str,
        depth: int,
    ) -> int:
        """Infer effective depth for leaf nodes when callers did not provide it.

        A ``depth`` value of ``0`` means "infer from the parent chain". Positive
        depths are already known and are returned unchanged.
        Returns ``1`` when the leaf's parent is a root-level issue (FEATURE depth)
        and ``2`` when the parent itself has a parent (TASK depth). When the parent
        chain extends beyond the configured depth cap, returns ``_MAX_DEPTH`` and
        emits the depth-cap warning. Non-numeric grandparent references are treated
        conservatively as TASK-depth leaves with a warning.

        Note:
            When ``depth`` is inferred (``depth == 0``), this method performs up to
            two additional ``get_parent()`` lookups (grandparent and
            great-grandparent).

        Args:
            owner: Repository owner.
            repo: Repository name.
            issue_number: Issue number being classified.
            parent: Parent issue reference.
            depth: Known depth from caller (0 means infer from parent chain).
        """
        if depth > 0:
            return depth

        try:
            parent_number = int(parent)
        except ValueError:
            print(
                f"Warning: Non-numeric parent reference {parent!r} for "
                f"{owner}/{repo}; defaulting leaf depth to FEATURE.",
                file=sys.stderr,
            )
            return 1

        try:
            grandparent = self.get_parent(owner, repo, parent_number)
        except HierarchyValidationError as exc:
            raise HierarchyValidationError(
                "api",
                f"Failed to determine grandparent for issue hierarchy depth inference: {exc}",
            ) from exc
        if grandparent is None:
            return 1

        try:
            grandparent_number = int(grandparent)
        except ValueError:
            print(
                f"Warning: Non-numeric grandparent reference {grandparent!r} for "
                f"{owner}/{repo}; defaulting leaf depth to TASK (depth=2).",
                file=sys.stderr,
            )
            return 2

        try:
            great_grandparent = self.get_parent(owner, repo, grandparent_number)
        except HierarchyValidationError as exc:
            raise HierarchyValidationError(
                "api",
                f"Failed to determine great-grandparent for issue hierarchy depth inference: {exc}",
            ) from exc

        if great_grandparent is not None:
            print(
                f"Warning: Hierarchy depth exceeds {_MAX_DEPTH} levels for "
                f"{owner}/{repo}#{issue_number}. Classifying as TASK (depth={_MAX_DEPTH}).",
                file=sys.stderr,
            )
            return _MAX_DEPTH

        return 2

    def _classify_level(
        self,
        owner: str,
        repo: str,
        issue_number: int,
        children: list[ChildEntry],
        parent: str | None,
        _depth: int,
    ) -> HierarchyLevel:
        """Classify hierarchy level from pre-fetched children and parent data.

        This is the canonical classification implementation used by both
        ``get_level()`` and ``build_hierarchy_tree()``, which avoids redundant
        API calls when children/parent are already known.

        Depth cap enforcement lives here so the behavior is consistent across
        all call sites. Leaf depth (when no children) is inferred by
        ``_infer_leaf_depth()``, which checks the grandparent to distinguish
        FEATURE-level leaves (parent has no grandparent) from TASK-level ones.

        Args:
            owner: Repository owner.
            repo: Repository name.
            issue_number: Issue number being classified.
            children: Pre-fetched list of child entries.
            parent: Pre-fetched parent reference string, or None if standalone
                or not applicable (e.g. when children are present).
            _depth: Hierarchy depth counter.

        Returns:
            HierarchyLevel classification.
        """
        # Depth cap — single enforcement point for all call sites
        if _depth >= _MAX_DEPTH:
            print(
                f"Warning: Hierarchy depth exceeds {_MAX_DEPTH} levels for "
                f"{owner}/{repo}#{issue_number}. Classifying as TASK.",
                file=sys.stderr,
            )
            return HierarchyLevel.TASK

        if parent is not None and children:
            if self._infer_leaf_depth(owner, repo, issue_number, parent, _depth) >= _MAX_DEPTH:
                return HierarchyLevel.TASK

        if children:
            # Primary classification: check if any child has its own children
            # Filter out cross-repo children (qualified keys with '/')
            same_repo_numbers = []
            for child in children:
                if "/" not in child.key:
                    try:
                        same_repo_numbers.append(int(child.key))
                    except ValueError:
                        pass

            if same_repo_numbers:
                try:
                    child_status = self._batch_check_children_have_children(owner, repo, same_repo_numbers)
                    if any(child_status.values()):
                        return HierarchyLevel.EPIC
                    return HierarchyLevel.FEATURE
                except HierarchyValidationError:
                    # Conservative fallback
                    print(
                        f"Warning: Batch child-status query failed for {owner}/{repo}#{issue_number}. "
                        "Classifying as FEATURE (conservative fallback).",
                        file=sys.stderr,
                    )
                    return HierarchyLevel.FEATURE
            else:
                # All children are cross-repo - classify as FEATURE
                return HierarchyLevel.FEATURE

        # No children - use depth-based classification
        if parent is None:
            # Standalone issue with no relationships
            return HierarchyLevel.TASK

        inferred_depth = self._infer_leaf_depth(owner, repo, issue_number, parent, _depth)
        if inferred_depth == 1:
            return HierarchyLevel.FEATURE
        return HierarchyLevel.TASK

    def build_hierarchy_tree(
        self,
        owner: str,
        repo: str,
        issue_number: int,
        *,
        _visited: set[str] | None = None,
        _depth: int = 0,
    ) -> HierarchyNode:
        """Build a complete hierarchy node for an issue.

        Combines title fetch, parent detection, child enumeration, and level
        classification into a single HierarchyNode.

        Args:
            owner: Repository owner.
            repo: Repository name.
            issue_number: Issue number to build node for.
            _visited: Internal cycle detection set (do not pass externally).
            _depth: Internal depth counter (do not pass externally).

        Returns:
            Fully populated HierarchyNode.

        Raises:
            HierarchyValidationError: On circular references or API failures.
        """
        if _visited is None:
            _visited = set()

        issue_ref = f"{owner}/{repo}#{issue_number}"

        # Cycle detection
        if issue_ref in _visited:
            raise HierarchyValidationError(
                "hierarchy",
                f"Circular reference detected: {issue_ref} was already visited",
            )
        _visited.add(issue_ref)

        title = self._fetch_issue_title(owner, repo, issue_number)
        parent = self.get_parent(owner, repo, issue_number)
        children = self.get_children(owner, repo, issue_number)
        # _classify_level handles depth-cap enforcement and reuses pre-fetched data
        level = self._classify_level(owner, repo, issue_number, children, parent, _depth)

        return HierarchyNode(
            title=title,
            level=level,
            parent=parent,
            children=children,
            processed_at=datetime.now(timezone.utc),
        )

    def detect_hierarchy(self, issue_key: str) -> HierarchyNode:
        """Detect and construct hierarchy node from issue metadata.

        Implements the ``HierarchyDetector`` protocol. Parses the issue key,
        resolves owner/repo, and delegates to ``build_hierarchy_tree()``.

        Args:
            issue_key: Issue identifier (bare number, #-prefixed, or qualified).

        Returns:
            HierarchyNode representing the issue with its determined level.

        Raises:
            HierarchyValidationError: If hierarchy cannot be determined.
        """
        try:
            owner, repo, issue_number = parse_issue_reference(issue_key, self.owner, self.repo)
        except ValueError as exc:
            raise HierarchyValidationError("issue_key", str(exc)) from exc
        return self.build_hierarchy_tree(owner, repo, issue_number)


_JIRA_NOT_IMPLEMENTED_MSG = "Jira hierarchy detection is not yet implemented. See issue #1857 for tracking."


class JiraHierarchyDetector:
    """Jira hierarchy detector stub.

    Intended to detect hierarchy from Jira issue metadata using the ``parent``
    field for direct parent relationships and ``customfield_10008`` for epic
    link associations. When fully implemented, this class will query the Jira
    REST API to resolve parent/child relationships and determine hierarchy
    levels (Epic, Feature, Task) based on issue type and link structure.

    All methods currently raise ``NotImplementedError`` as this is a stub
    placeholder for future Jira integration.
    """

    def detect_hierarchy(self, issue_key: str) -> HierarchyNode:
        """Detect hierarchy from Jira issue metadata.

        When implemented, will query Jira REST API for the given issue key,
        resolve parent via the ``parent`` field and epic via
        ``customfield_10008``, determine children from sub-task links, and
        return a fully populated ``HierarchyNode``.

        Args:
            issue_key: Jira issue key (e.g., "PROJECT-123").

        Raises:
            NotImplementedError: Always, until Jira integration is complete.
        """
        raise NotImplementedError(_JIRA_NOT_IMPLEMENTED_MSG)

    def get_parent(self, *args: Any, **kwargs: Any) -> str | None:
        """Retrieve the parent issue key from Jira.

        When implemented, will use the ``parent`` field on the Jira issue
        to determine the direct parent relationship.
        """
        raise NotImplementedError(_JIRA_NOT_IMPLEMENTED_MSG)

    def get_children(self, *args: Any, **kwargs: Any) -> list[ChildEntry]:
        """Retrieve child issues from Jira.

        When implemented, will query sub-task links and epic-child
        relationships to build the ordered list of children.
        """
        raise NotImplementedError(_JIRA_NOT_IMPLEMENTED_MSG)

    def get_level(self, *args: Any, **kwargs: Any) -> HierarchyLevel:
        """Determine the hierarchy level of a Jira issue.

        When implemented, will classify the issue as Epic, Feature, or Task
        based on issue type and link structure.
        """
        raise NotImplementedError(_JIRA_NOT_IMPLEMENTED_MSG)

    def build_hierarchy_tree(self, *args: Any, **kwargs: Any) -> HierarchyNode:
        """Build a full hierarchy tree from a Jira issue.

        When implemented, will combine parent, children, and level detection
        to construct a complete ``HierarchyNode`` tree.
        """
        raise NotImplementedError(_JIRA_NOT_IMPLEMENTED_MSG)


def get_hierarchy_detector(provider: object, **kwargs: Any) -> HierarchyDetector:
    """Factory function to obtain a hierarchy detector by provider name.

    Args:
        provider: The provider identifier. Must be ``"github"`` or ``"jira"``
            (case-sensitive string matching).
        **kwargs: Provider-specific keyword arguments passed to the detector
            constructor (e.g., ``owner`` and ``repo`` for GitHub).

    Returns:
        A ``HierarchyDetector`` instance for the specified provider.

    Raises:
        ValueError: If the provider is not recognized.
    """
    if provider == "github":
        return GitHubHierarchyDetector(**kwargs)
    if provider == "jira":
        return JiraHierarchyDetector(**kwargs)

    raise ValueError(f"Unsupported hierarchy provider: {provider!r}. Valid providers: github, jira")
