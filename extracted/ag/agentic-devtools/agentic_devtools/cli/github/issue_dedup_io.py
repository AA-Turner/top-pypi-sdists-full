"""GitHub I/O layer for the error-signature dedup engine.

Provides search, reaction, and comment operations for issue deduplication.
All GitHub API calls go through the ``gh`` CLI via ``run_safe`` with
``shell=False`` for safety.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.parse

from agentic_devtools.cli.shared.retry import (
    RetryableError,
    retry_with_backoff,
)

from ..subprocess_utils import run_safe
from .issue_dedup import build_search_query
from .repo_resolution import resolve_github_repo


def _gh_api(
    endpoint: str,
    *,
    method: str = "GET",
    body: dict | None = None,
    headers: dict[str, str] | None = None,
) -> str:
    """Call the GitHub API via the ``gh`` CLI.

    Args:
        endpoint: API endpoint path (e.g., "/repos/{owner}/{repo}/issues/1").
        method: HTTP method.
        body: JSON body for POST/PATCH/PUT requests.
        headers: Optional HTTP headers passed via repeated ``-H`` args.

    Returns:
        Raw response body as string.

    Raises:
        RetryableError: On rate limit (HTTP 403/429) or transient failure.
        RuntimeError: On non-retryable API errors.
    """
    cmd = ["gh", "api", endpoint, "--method", method]
    if body is not None:
        cmd.extend(["--input", "-"])
    if headers:
        for key, value in headers.items():
            cmd.extend(["-H", f"{key}: {value}"])

    result = run_safe(
        cmd,
        capture_output=True,
        text=True,
        shell=False,
        input=json.dumps(body) if body is not None else None,
    )

    if result.returncode != 0:
        stderr = result.stderr.strip()
        # Detect secondary rate limit
        if "secondary rate limit" in stderr.lower() or "rate limit" in stderr.lower():
            raise RetryableError(
                f"Rate limited: {stderr}",
                provider="github",
                is_rate_limit=True,
            )
        if result.returncode == 4:  # gh CLI uses exit 4 for HTTP 4xx
            raise RuntimeError(f"GitHub API error: {stderr}")
        raise RuntimeError(f"gh api failed (exit {result.returncode}): {stderr}")

    return result.stdout


def search_by_marker(sig: str, *, repo: str | None = None) -> list[dict]:
    """Search GitHub issues by dedup marker signature.

    Paginates through all results using ``per_page=100``.  Transient
    rate-limit errors are retried at the per-page level so that pages
    already collected are not lost.

    Args:
        sig: The dedup signature to search for.
        repo: Optional ``owner/repo`` override.
            Resolved via ``resolve_github_repo()`` if not provided.

    Returns:
        List of issue dicts from the search results.

    Raises:
        RuntimeError: On non-retryable API errors (propagated from
            ``_search_api_call`` for fail-fast dedup policy).
        ProviderRateLimitError: After retry exhaustion on rate limits
            (raised by the per-page retry in ``_search_api_call``).
    """
    resolved_repo = resolve_github_repo(repo)
    query = build_search_query(sig)
    full_query = f"{query} repo:{resolved_repo}"
    encoded_query = urllib.parse.quote(full_query, safe="")

    all_items: list[dict] = []
    page = 1
    per_page = 100

    while True:
        endpoint = f"/search/issues?q={encoded_query}&per_page={per_page}&page={page}"
        try:
            raw = _search_api_call(endpoint)
        except RuntimeError:
            raise  # Propagate to caller for fail-fast dedup policy

        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            print(
                "Warning: Malformed JSON response from GitHub search API",
                file=sys.stderr,
            )
            return []

        if not isinstance(data, dict):
            print(
                "Warning: Unexpected response format from GitHub search API",
                file=sys.stderr,
            )
            return []

        items = data.get("items")
        if not isinstance(items, list):
            print(
                "Warning: Missing or invalid 'items' in search response",
                file=sys.stderr,
            )
            return []

        if not items:
            break

        all_items.extend(items)

        if len(items) < per_page:
            break

        page += 1

    return all_items


@retry_with_backoff(
    initial_delay=5.0,
    max_delay=5.0,
    max_retries=3,
    jitter_factor=0.0,
)
def _search_api_call(endpoint: str) -> str:
    """Execute a single search API call with fixed 5-second backoff retry.

    Extracted so the retry decorator wraps the per-page call rather than
    the entire pagination loop, preserving already-collected pages on
    transient failures.
    """
    return _gh_api(endpoint)


def add_thumbs_up(issue_number: int, *, repo: str | None = None) -> None:
    """Add a +1 reaction to an issue if not already reacted.

    Fetches the authenticated user, checks existing reactions for a prior
    ``+1`` by that user, and skips the POST if already reacted.

    Args:
        issue_number: The issue number to react to.
        repo: Optional ``owner/repo`` override.

    Raises:
        RuntimeError: When the issue is inaccessible or API calls fail.
    """
    resolved_repo = resolve_github_repo(repo)

    # Get authenticated user
    user_response = _gh_api("/user")
    try:
        user_data = json.loads(user_response)
        username = user_data.get("login", "")
    except (json.JSONDecodeError, TypeError) as exc:
        raise RuntimeError("Failed to resolve authenticated user") from exc

    if not username:
        raise RuntimeError("Failed to resolve authenticated user login")

    # Check existing reactions (paginated)
    already_reacted = False
    page = 1
    per_page = 100

    while True:
        endpoint = f"/repos/{resolved_repo}/issues/{issue_number}/reactions?per_page={per_page}&page={page}"
        try:
            raw = _gh_api(endpoint)
        except RuntimeError as exc:
            raise RuntimeError(f"Issue #{issue_number} is inaccessible: {exc}") from exc

        try:
            reactions = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            break

        if not isinstance(reactions, list):
            break

        for reaction in reactions:
            if (
                isinstance(reaction, dict)
                and reaction.get("content") == "+1"
                and isinstance(reaction.get("user"), dict)
                and reaction["user"].get("login") == username
            ):
                already_reacted = True
                break

        if already_reacted or len(reactions) < per_page:
            break

        page += 1

    if already_reacted:
        return

    # POST +1 reaction
    _gh_api(
        f"/repos/{resolved_repo}/issues/{issue_number}/reactions",
        method="POST",
        body={"content": "+1"},
    )


def add_augment_comment(issue_number: int, body: str, *, repo: str | None = None) -> None:
    """Add an augmentation comment to an issue with fenced body.

    The body is wrapped in tilde fences to preserve formatting
    and prevent accidental markdown interpretation. The fence length
    is selected dynamically to avoid collisions with fence-like content
    inside ``body``.

    Args:
        issue_number: The issue number to comment on.
        body: The comment body (preserved verbatim inside fences).
        repo: Optional ``owner/repo`` override.

    Raises:
        RuntimeError: When the API call fails.
    """
    resolved_repo = resolve_github_repo(repo)
    max_body_tilde_run = max((len(match.group(0)) for match in re.finditer(r"~+", body)), default=0)
    fence = "~" * max(4, max_body_tilde_run + 1)
    separator = "" if body.endswith("\n") else "\n"
    fenced_body = f"{fence}\n{body}{separator}{fence}"
    _gh_api(
        f"/repos/{resolved_repo}/issues/{issue_number}/comments",
        method="POST",
        body={"body": fenced_body},
    )
