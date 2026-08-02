"""Fetch release metadata from the GitHub API (authenticated when a token is present)."""

import os

import httpx


def github_headers() -> dict[str, str]:
    """Authorization + API-version headers for api.github.com; auth only when a token is set.

    Unauthenticated GitHub API is capped at 60 requests/hour per IP. On shared CI runners
    that quota is exhausted quickly and version checks start failing with HTTP 403
    ("accès refusés"). A token (``GITHUB_TOKEN`` or ``GH_TOKEN`` — the conventional names,
    the latter also set by the ``gh`` CLI) lifts the cap to 5000 requests/hour. Read-only
    public access, so a tokenless run still works until it hits the rate limit.
    """
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def github_get(url: str, timeout: float = 10.0) -> httpx.Response:
    """GET a GitHub API URL with auth headers when available; raise on HTTP error."""
    response = httpx.get(url, timeout=timeout, follow_redirects=True, headers=github_headers())
    response.raise_for_status()
    return response


def latest_release(repo: str, timeout: float = 10.0) -> str:
    """Return the tag_name of the latest release for `owner/repo`.

    Raises httpx.HTTPError on network failure.
    """
    response = github_get(f"https://api.github.com/repos/{repo}/releases/latest", timeout=timeout)
    data = response.json()
    tag = data.get("tag_name", "")
    if not isinstance(tag, str):
        raise ValueError(f"Unexpected tag_name type: {type(tag).__name__}")
    return tag
