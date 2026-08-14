# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""GitHub API utilities.

This module provides core utilities for interacting with GitHub's REST API,
including authentication, user/comment operations, PR information retrieval,
and file content fetching. These utilities are used by MCP tools and other
modules but are not MCP-specific.
"""

from __future__ import annotations

import datetime
import functools
import os
import re
import shutil
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Literal, overload
from urllib.parse import urlparse

import requests
from github import Auth, Github, GithubException
from github.Repository import Repository
from pydantic import BaseModel, Field, JsonValue, TypeAdapter, ValidationError

GITHUB_API_BASE = "https://api.github.com"


def _get_gh_cli_token() -> str | None:
    """Get a GitHub token from the `gh` CLI, or `None` if unavailable.

    On Devin machines this returns the GitHub App Installation token which
    typically has broad org access, including private repositories.
    """
    gh_path = shutil.which("gh")
    if not gh_path:
        return None
    try:
        result = subprocess.run(
            [gh_path, "auth", "token"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        pass
    return None


@overload
def resolve_default_github_token(*, allow_none: Literal[False] = False) -> str: ...


@overload
def resolve_default_github_token(*, allow_none: Literal[True]) -> str | None: ...


@overload
def resolve_default_github_token(*, allow_none: bool) -> str | None: ...


def resolve_default_github_token(*, allow_none: bool = False) -> str | None:
    """Resolve the default GitHub token for general API access.

    Priority order:
    1. `gh auth token` — Devin's GitHub App Installation token, which
       typically has broad org access including private repositories.
    2. `GITHUB_TOKEN` environment variable — fallback.

    Use this for read-only operations (fetching comments, user profiles,
    PR info, workflow status, etc.).  For *triggering* CI workflows use
    :func:`resolve_ci_trigger_github_token` instead.

    Returns a GitHub token string. When `allow_none` is `True`, returns `None`
    if no token is found instead of raising.
    """
    gh_token = _get_gh_cli_token()
    if gh_token:
        return gh_token

    token = os.getenv("GITHUB_TOKEN")
    if token:
        return token

    if allow_none:
        return None

    raise ValueError(
        "No GitHub token found. Authenticate with 'gh auth login' "
        "or set the GITHUB_TOKEN environment variable."
    )


_CI_TRIGGER_TOKEN_ENV_VARS = ["GITHUB_CI_WORKFLOW_TRIGGER_PAT", "GITHUB_TOKEN"]
_COPILOT_REVIEW_TOKEN_ENV_VARS = ["GITHUB_CI_WORKFLOW_TRIGGER_PAT"]
COPILOT_REVIEWER_LOGIN = "copilot-pull-request-reviewer"


class AgentEnum(StrEnum):
    """AI reviewer targets supported by pull request review requests."""

    DEFAULT = "DEFAULT"
    Copilot = "Copilot"  # Casing is the reviewer-facing wire value.


_REVIEWER_LOGIN_BY_AGENT = {
    AgentEnum.Copilot: COPILOT_REVIEWER_LOGIN,
}


def resolve_ci_trigger_github_token(
    preferred_env_vars: list[str] | None = None,
) -> str:
    """Resolve a GitHub token for triggering CI workflows.

    Priority order:
    1. Environment variables in *preferred_env_vars* order (defaults to
       `GITHUB_CI_WORKFLOW_TRIGGER_PAT`, `GITHUB_TOKEN`).
    2. `gh auth token` as a last-resort fallback.

    Use this **only** for workflow-dispatch operations that require
    `actions:write` permission.  For general GitHub API access use
    :func:`resolve_default_github_token` instead.

    Args:
        preferred_env_vars: Environment variable names to check, in order.
            Defaults to `["GITHUB_CI_WORKFLOW_TRIGGER_PAT", "GITHUB_TOKEN"]`.
            Callers with a specialised PAT (e.g. `GITHUB_CONNECTOR_PUBLISHING_PAT`)
            can override this list.

    Returns:
        GitHub token string.

    Raises:
        ValueError: If no GitHub token is found.
    """
    if preferred_env_vars is None:
        preferred_env_vars = list(_CI_TRIGGER_TOKEN_ENV_VARS)

    for env_var in preferred_env_vars:
        token = os.getenv(env_var)
        if token:
            return token

    # Last-resort fallback to gh CLI
    gh_token = _get_gh_cli_token()
    if gh_token:
        return gh_token

    env_var_list = ", ".join(preferred_env_vars)
    raise ValueError(
        f"No GitHub token found. Set one of: {env_var_list} environment variable, "
        "or authenticate with 'gh auth login'."
    )


def resolve_copilot_review_github_token() -> str:
    """Resolve the dedicated user PAT used for Copilot review requests.

    The resolved PAT must belong to a real GitHub user with a Copilot seat.
    This resolver intentionally does not fall back to the GitHub App token,
    `GITHUB_TOKEN`, or `gh auth token`, because those identities silently
    accept review requests without adding Copilot.

    Raises:
        ValueError: If the approved PAT environment variable is not configured.
    """
    for env_var in _COPILOT_REVIEW_TOKEN_ENV_VARS:
        token = os.getenv(env_var)
        if token:
            return token

    raise ValueError(
        "GitHub Copilot review PAT is not configured. "
        "Set the GITHUB_CI_WORKFLOW_TRIGGER_PAT environment variable."
    )


@dataclass(frozen=True)
class AIReviewRequestResult:
    """Result of requesting and verifying AI reviewers."""

    requested: bool
    reviewers: list[str]
    message: str


class _PullRequestNode(BaseModel):
    id: str


class _PullRequestRepository(BaseModel):
    pull_request: _PullRequestNode = Field(alias="pullRequest")


class _PullRequestNodeData(BaseModel):
    repository: _PullRequestRepository


class _RequestedReviewer(BaseModel):
    reviewer_type: str = Field(alias="__typename")
    login: str | None = None


class _ReviewRequestNode(BaseModel):
    requested_reviewer: _RequestedReviewer | None = Field(alias="requestedReviewer")


class _ReviewRequests(BaseModel):
    nodes: list[_ReviewRequestNode]


class _ReviewPullRequest(BaseModel):
    review_requests: _ReviewRequests = Field(alias="reviewRequests")


class _ReviewRepository(BaseModel):
    pull_request: _ReviewPullRequest = Field(alias="pullRequest")


class _ReviewRequestsData(BaseModel):
    repository: _ReviewRepository


class _CopilotBot(BaseModel):
    node_id: str
    bot_type: str = Field(alias="type")


_JSON_OBJECT_ADAPTER = TypeAdapter(dict[str, JsonValue])


def _graphql_request(
    query: str,
    variables: Mapping[str, object],
    token: str,
) -> dict[str, JsonValue]:
    """Execute a GitHub GraphQL request and return its `data` object."""
    response = requests.post(
        f"{GITHUB_API_BASE}/graphql",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={"query": query, "variables": variables},
        timeout=30,
    )
    response.raise_for_status()
    try:
        payload = _JSON_OBJECT_ADAPTER.validate_python(response.json())
    except ValidationError as error:
        raise GitHubAPIError("Unexpected response from GitHub GraphQL API") from error
    errors = payload.get("errors")
    if errors:
        raise GitHubAPIError(f"GitHub GraphQL request failed: {errors}")
    try:
        return _JSON_OBJECT_ADAPTER.validate_python(payload.get("data"))
    except ValidationError as error:
        raise GitHubAPIError("Unexpected response from GitHub GraphQL API") from error


def _normalize_review_targets(
    request_to: AgentEnum | list[AgentEnum],
) -> list[AgentEnum]:
    if isinstance(request_to, AgentEnum):
        targets = [request_to]
    elif isinstance(request_to, list):
        targets = request_to
    else:
        raise ValueError(f"Unsupported AI reviewer: {request_to!r}")
    if not targets:
        raise ValueError("request_to must contain at least one supported reviewer")

    normalized: list[AgentEnum] = []
    for target in targets:
        if not isinstance(target, AgentEnum):
            raise ValueError(f"Unsupported AI reviewer: {target!r}")
        resolved = AgentEnum.Copilot if target is AgentEnum.DEFAULT else target
        if resolved not in _REVIEWER_LOGIN_BY_AGENT:
            raise ValueError(f"Unsupported AI reviewer: {target.value}")
        if resolved not in normalized:
            normalized.append(resolved)
    return normalized


def request_pr_ai_review(
    owner: str,
    repo: str,
    pr_number: int,
    token: str,
    request_to: AgentEnum | list[AgentEnum] = AgentEnum.DEFAULT,
) -> AIReviewRequestResult:
    """Request the selected AI reviews and verify the recorded requests.

    The Copilot reviewer is a bot. Resolve its node ID through the REST user
    endpoint, then pass it through `botIds` in the GraphQL mutation.
    """
    _normalize_review_targets(request_to)

    try:
        bot_id = _copilot_bot_node_id(token)
    except (GitHubAPIError, requests.RequestException, ValidationError) as error:
        return AIReviewRequestResult(
            requested=False,
            reviewers=[],
            message=(
                "GitHub could not resolve the Copilot reviewer bot. Confirm that "
                "the PAT's user has a Copilot seat and that the organization has "
                f"enabled Copilot code review. Details: {error}"
            ),
        )

    try:
        pull_request_id = _pull_request_node_id(owner, repo, pr_number, token)
    except (GitHubAPIError, requests.RequestException, ValidationError) as error:
        return AIReviewRequestResult(
            requested=False,
            reviewers=[],
            message=(
                "GitHub could not resolve the pull request. Confirm that the "
                "PAT is valid and can access the repository. Details: "
                f"{error}"
            ),
        )
    request_reviews_query = """
    mutation RequestReviews($input: RequestReviewsInput!) {
      requestReviews(input: $input) {
        clientMutationId
        pullRequest {
          number
        }
      }
    }
    """
    try:
        _graphql_request(
            request_reviews_query,
            {
                "input": {
                    "pullRequestId": pull_request_id,
                    "botIds": [bot_id],
                    "union": True,
                }
            },
            token,
        )
    except (GitHubAPIError, requests.RequestException, ValidationError) as error:
        return AIReviewRequestResult(
            requested=False,
            reviewers=[],
            message=(
                "GitHub rejected the Copilot review request. Confirm that the "
                "PAT's user has a Copilot seat and that the organization has "
                f"enabled Copilot code review. Details: {error}"
            ),
        )

    try:
        verified = _has_copilot_review_request(owner, repo, pr_number, token)
    except (GitHubAPIError, requests.RequestException, ValidationError) as error:
        return AIReviewRequestResult(
            requested=False,
            reviewers=[],
            message=(
                "GitHub may have recorded the Copilot review request, but it "
                "could not be confirmed through GraphQL reviewRequests. "
                f"Details: {error}"
            ),
        )

    if not verified:
        return AIReviewRequestResult(
            requested=False,
            reviewers=[],
            message=(
                "GitHub accepted the Copilot review request, but GraphQL "
                f"reviewRequests does not show it on {owner}/{repo} PR "
                f"{pr_number}. Confirm that the PAT's user has a Copilot seat "
                "and that the organization has enabled Copilot code review."
            ),
        )

    return AIReviewRequestResult(
        requested=True,
        reviewers=[_REVIEWER_LOGIN_BY_AGENT[AgentEnum.Copilot]],
        message=f"Copilot review requested for {owner}/{repo} PR {pr_number}.",
    )


def _pull_request_node_id(
    owner: str,
    repo: str,
    pr_number: int,
    token: str,
) -> str:
    """Fetch a pull request's GraphQL node ID."""
    data = _graphql_request(
        """
        query PullRequestNodeId($owner: String!, $name: String!, $number: Int!) {
          repository(owner: $owner, name: $name) {
            pullRequest(number: $number) {
              id
            }
          }
        }
        """,
        {"owner": owner, "name": repo, "number": pr_number},
        token,
    )
    parsed = _PullRequestNodeData.model_validate(data)
    return parsed.repository.pull_request.id


def _copilot_bot_node_id(token: str) -> str:
    """Resolve the Copilot review bot's GraphQL node ID."""
    response = requests.get(
        f"{GITHUB_API_BASE}/users/{COPILOT_REVIEWER_LOGIN}%5Bbot%5D",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=30,
    )
    response.raise_for_status()
    bot = _CopilotBot.model_validate(response.json())
    if bot.bot_type != "Bot":
        raise GitHubAPIError(
            "GitHub Copilot reviewer lookup did not return a bot node ID"
        )
    return bot.node_id


def _has_copilot_review_request(
    owner: str,
    repo: str,
    pr_number: int,
    token: str,
) -> bool:
    """Verify the Copilot bot appears in GraphQL `reviewRequests`.

    The REST `requested_reviewers` endpoint remains empty for this bot even
    after a successful request, so it must not be used for verification.
    """
    data = _graphql_request(
        """
        query PullRequestReviewRequests(
          $owner: String!
          $name: String!
          $number: Int!
        ) {
          repository(owner: $owner, name: $name) {
            pullRequest(number: $number) {
              reviewRequests(first: 100) {
                nodes {
                  requestedReviewer {
                    __typename
                    ... on Bot {
                      login
                    }
                  }
                }
              }
            }
          }
        }
        """,
        {"owner": owner, "name": repo, "number": pr_number},
        token,
    )
    parsed = _ReviewRequestsData.model_validate(data)

    return any(
        node.requested_reviewer is not None
        and node.requested_reviewer.reviewer_type == "Bot"
        and node.requested_reviewer.login == COPILOT_REVIEWER_LOGIN
        for node in parsed.repository.pull_request.review_requests.nodes
    )


def _resolve_all_default_github_tokens() -> list[str]:
    """Collect all available GitHub tokens in *default* priority order.

    Returns a deduplicated list with `gh auth token` first (broadest
    org access, likely to work on private repos), then `GITHUB_TOKEN`.

    This is used by :func:`get_github_comment_info` to retry on 404
    with a different token when the first one lacks access to a private
    repository.
    """
    tokens: list[str] = []
    seen: set[str] = set()

    # gh CLI token first — broadest access (Devin's installation token)
    gh_token = _get_gh_cli_token()
    if gh_token:
        tokens.append(gh_token)
        seen.add(gh_token)

    # Then GITHUB_TOKEN env var
    env_token = os.getenv("GITHUB_TOKEN")
    if env_token and env_token not in seen:
        tokens.append(env_token)
        seen.add(env_token)

    return tokens


@dataclass
class PRHeadInfo:
    """Information about a PR's head commit."""

    ref: str
    """Branch name of the PR's head"""

    sha: str
    """Full commit SHA of the PR's head"""

    short_sha: str
    """First 7 characters of the commit SHA"""


def get_pr_head_ref(
    owner: str,
    repo: str,
    pr_number: int,
    token: str,
) -> PRHeadInfo:
    """Get the head ref (branch name) and SHA for a PR.

    This is useful for resolving a PR number to the actual branch name,
    which is required for workflow_dispatch API calls (which don't accept
    refs/pull/{pr}/head format).

    Args:
        owner: Repository owner (e.g., "airbytehq")
        repo: Repository name (e.g., "airbyte")
        pr_number: Pull request number
        token: GitHub API token

    Returns:
        PRHeadInfo with ref (branch name), sha, and short_sha.

    Raises:
        ValueError: If PR not found.
        requests.HTTPError: If API request fails.
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 404:
        raise ValueError(f"PR {owner}/{repo}#{pr_number} not found")
    response.raise_for_status()

    pr_data = response.json()
    sha = pr_data["head"]["sha"]
    return PRHeadInfo(
        ref=pr_data["head"]["ref"],
        sha=sha,
        short_sha=sha[:7],
    )


@functools.lru_cache(maxsize=32)
def _get_github_repo(owner: str, repo: str, token: str) -> Repository:
    """Get a cached GitHub repository object.

    This function caches repository objects to avoid redundant API calls
    when fetching multiple PRs from the same repository. Uses lazy=True
    to avoid making an API call just to create the repo object.
    """
    auth = Auth.Token(token)
    gh = Github(auth=auth)
    return gh.get_repo(f"{owner}/{repo}", lazy=True)


def get_pr_merge_date(
    owner: str,
    repo: str,
    pr_number: int,
    token: str | None = None,
) -> datetime.date | None:
    """Get the merge date for a PR.

    Args:
        owner: Repository owner (e.g., "airbytehq")
        repo: Repository name (e.g., "airbyte")
        pr_number: Pull request number
        token: GitHub API token. If None, will be resolved from environment.

    Returns:
        The date the PR was merged, or None if not merged.

    Raises:
        GitHubAPIError: If the API request fails.
    """
    if token is None:
        token = resolve_default_github_token()

    try:
        gh_repo = _get_github_repo(owner, repo, token)
        pr = gh_repo.get_pull(pr_number)
    except GithubException as e:
        if e.status == 404:
            raise GitHubAPIError(f"PR {owner}/{repo}#{pr_number} not found") from e
        raise GitHubAPIError(
            f"Failed to fetch PR {owner}/{repo}#{pr_number}: {e.status} {e.data}"
        ) from e

    if pr.merged_at is None:
        return None

    return pr.merged_at.date()


def get_file_contents_at_ref(
    owner: str,
    repo: str,
    path: str,
    ref: str,
    token: str | None = None,
) -> str | None:
    """Fetch file contents from GitHub at a specific ref.

    Uses the GitHub Contents API to retrieve file contents at a specific
    commit SHA, branch, or tag. This allows reading files without having
    the repository checked out locally.

    Args:
        owner: Repository owner (e.g., "airbytehq")
        repo: Repository name (e.g., "airbyte")
        path: Path to the file within the repository
        ref: Git ref (commit SHA, branch name, or tag)
        token: GitHub API token (optional for public repos, but recommended
            to avoid rate limiting)

    Returns:
        File contents as a string, or None if the file doesn't exist.

    Raises:
        requests.HTTPError: If API request fails (except 404).
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}"
    headers = {
        "Accept": "application/vnd.github.raw+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    params = {"ref": ref}

    response = requests.get(url, headers=headers, params=params, timeout=30)
    if response.status_code == 404:
        return None
    response.raise_for_status()

    return response.text


def get_pr_changed_files(
    owner: str,
    repo: str,
    pr_number: int,
    token: str | None = None,
) -> list[str]:
    """Get the list of files changed in a pull request via the GitHub API.

    Uses the `GET /repos/{owner}/{repo}/pulls/{pr_number}/files` endpoint
    and paginates through all pages (GitHub returns at most 30 files per page
    by default; we request 100 per page to minimise round-trips).

    This avoids any dependency on local git history or shallow-clone depth,
    making it the most reliable way to determine which files a PR touches.

    Args:
        owner: Repository owner (e.g., `"airbytehq"`).
        repo: Repository name (e.g., `"airbyte"`).
        pr_number: Pull request number.
        token: GitHub API token.  If `None`, resolved from the environment
            via :func:`resolve_default_github_token`.

    Returns:
        Sorted, deduplicated list of file paths changed in the PR.

    Raises:
        GitHubAPIError: If the API request fails.
    """
    if token is None:
        token = resolve_default_github_token()

    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    all_files: list[str] = []
    page = 1
    try:
        while True:
            params = {"per_page": 100, "page": page}
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if not response.ok:
                raise GitHubAPIError(
                    f"Failed to fetch changed files for PR {owner}/{repo}#{pr_number}: "
                    f"{response.status_code} {response.text}"
                )
            data = response.json()
            if not data:
                break
            all_files.extend(item["filename"] for item in data)
            if len(data) < 100:
                break
            page += 1
    except requests.exceptions.RequestException as exc:
        raise GitHubAPIError(
            f"Network error while fetching changed files for PR {owner}/{repo}#{pr_number}"
        ) from exc
    except (ValueError, KeyError) as exc:
        raise GitHubAPIError(
            f"Unexpected response from GitHub while fetching changed files for "
            f"PR {owner}/{repo}#{pr_number}"
        ) from exc

    return sorted(set(all_files))


class GitHubCommentParseError(Exception):
    """Raised when a GitHub comment URL cannot be parsed."""


class GitHubUserEmailNotFoundError(Exception):
    """Raised when a GitHub user's public email cannot be found."""


class GitHubAPIError(Exception):
    """Raised when a GitHub API call fails."""


@dataclass(frozen=True)
class GitHubCommentInfo:
    """Information about a GitHub comment and its author."""

    comment_id: int
    """The numeric comment ID."""

    owner: str
    """Repository owner (e.g., 'airbytehq')."""

    repo: str
    """Repository name (e.g., 'oncall')."""

    author_login: str
    """GitHub username of the comment author."""

    author_association: str
    """Author's association with the repo (e.g., 'MEMBER', 'OWNER', 'CONTRIBUTOR')."""

    comment_type: str
    """Type of comment: 'issue_comment' or 'review_comment'."""


@dataclass(frozen=True)
class GitHubUserInfo:
    """Information about a GitHub user."""

    login: str
    """GitHub username."""

    email: str | None
    """Public email address, if set."""

    name: str | None
    """Display name, if set."""


def _parse_github_comment_url(url: str) -> tuple[str, str, int, str]:
    """Parse a GitHub comment URL to extract owner, repo, comment_id, and comment_type.

    Supports two URL formats:
    - Issue/PR timeline comments: https://github.com/{owner}/{repo}/issues/{num}#issuecomment-{id}
    - PR review comments: https://github.com/{owner}/{repo}/pull/{num}#discussion_r{id}

    Args:
        url: GitHub comment URL.

    Returns:
        Tuple of (owner, repo, comment_id, comment_type).
        comment_type is either 'issue_comment' or 'review_comment'.

    Raises:
        GitHubCommentParseError: If the URL cannot be parsed.
    """
    parsed = urlparse(url)

    if parsed.scheme != "https":
        raise GitHubCommentParseError(
            f"Invalid URL scheme: expected 'https', got '{parsed.scheme}'"
        )

    if parsed.netloc != "github.com":
        raise GitHubCommentParseError(
            f"Invalid URL host: expected 'github.com', got '{parsed.netloc}'"
        )

    path_parts = parsed.path.strip("/").split("/")
    if len(path_parts) < 2:
        raise GitHubCommentParseError(
            f"Invalid URL path: expected at least owner/repo, got '{parsed.path}'"
        )

    owner = path_parts[0]
    repo = path_parts[1]
    fragment = parsed.fragment

    issue_comment_match = re.match(r"^issuecomment-(\d+)$", fragment)
    if issue_comment_match:
        comment_id = int(issue_comment_match.group(1))
        return owner, repo, comment_id, "issue_comment"

    review_comment_match = re.match(r"^discussion_r(\d+)$", fragment)
    if review_comment_match:
        comment_id = int(review_comment_match.group(1))
        return owner, repo, comment_id, "review_comment"

    raise GitHubCommentParseError(
        f"Invalid URL fragment: expected '#issuecomment-<id>' or '#discussion_r<id>', "
        f"got '#{fragment}'"
    )


def get_github_comment_info(
    owner: str,
    repo: str,
    comment_id: int,
    comment_type: str,
    token: str | None = None,
) -> GitHubCommentInfo:
    """Fetch comment information from GitHub API.

    When no explicit token is provided, all available tokens are tried in
    priority order.  This handles the case where the first token lacks
    access to a private repository (GitHub returns 404 for repos the
    token cannot access) but a later token—such as the one from
    `gh auth token`—does have access.

    Args:
        owner: Repository owner.
        repo: Repository name.
        comment_id: Numeric comment ID.
        comment_type: Either 'issue_comment' or 'review_comment'.
        token: GitHub API token. If None, will be resolved from environment.

    Returns:
        GitHubCommentInfo with comment and author details.

    Raises:
        GitHubAPIError: If the API request fails.
        ValueError: If comment_type is invalid.
    """
    if comment_type == "issue_comment":
        url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues/comments/{comment_id}"
    elif comment_type == "review_comment":
        url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls/comments/{comment_id}"
    else:
        raise ValueError(f"Invalid comment_type: {comment_type}")

    # When an explicit token is provided, use only that token.
    # Otherwise try all available default tokens so that private-repo
    # 404s can be resolved by a token with broader access.
    if token is not None:
        tokens_to_try = [token]
    else:
        tokens_to_try = _resolve_all_default_github_tokens()
        if not tokens_to_try:
            raise GitHubAPIError(
                "No GitHub token found. Authenticate with 'gh auth login' "
                "or set the GITHUB_TOKEN environment variable."
            )

    last_status: int = 0
    last_body: str = ""
    for t in tokens_to_try:
        headers = {
            "Authorization": f"Bearer {t}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        response = requests.get(url, headers=headers, timeout=30)
        if response.ok:
            data = response.json()
            user = data.get("user", {})
            return GitHubCommentInfo(
                comment_id=comment_id,
                owner=owner,
                repo=repo,
                author_login=user.get("login", ""),
                author_association=data.get("author_association", "NONE"),
                comment_type=comment_type,
            )

        last_status = response.status_code
        last_body = response.text

        # 404 may mean the token lacks access to a private repo;
        # try the next token before giving up.
        if response.status_code == 404:
            continue

        # For non-404 errors, fail immediately.
        raise GitHubAPIError(
            f"Failed to fetch comment {comment_id} from {owner}/{repo}: "
            f"{last_status} {last_body}"
        )

    # All tokens exhausted (all returned 404).
    num_tokens = len(tokens_to_try)
    raise GitHubAPIError(
        f"Failed to fetch comment {comment_id} from {owner}/{repo}: "
        f"{last_status} (not found or insufficient token permissions "
        f"for private repo). Tried {num_tokens} token(s)."
    )


def get_github_user_info(login: str, token: str | None = None) -> GitHubUserInfo:
    """Fetch user information from GitHub API.

    Args:
        login: GitHub username.
        token: GitHub API token. If None, will be resolved from environment.

    Returns:
        GitHubUserInfo with user details.

    Raises:
        GitHubAPIError: If the API request fails.
    """
    if token is None:
        token = resolve_default_github_token()

    url = f"{GITHUB_API_BASE}/users/{login}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.get(url, headers=headers, timeout=30)
    if not response.ok:
        raise GitHubAPIError(
            f"Failed to fetch user {login}: {response.status_code} {response.text}"
        )

    data = response.json()

    return GitHubUserInfo(
        login=data.get("login", login),
        email=data.get("email"),
        name=data.get("name"),
    )


def get_admin_email_from_approval_comment(approval_comment_url: str) -> str:
    """Derive the admin email from a GitHub approval comment URL.

    This function:
    1. Parses the comment URL to extract owner, repo, and comment ID.
    2. Fetches the comment from GitHub API to get the author's username.
    3. Fetches the user's profile to get their public email.
    4. Validates the email is an @airbyte.io address.

    Args:
        approval_comment_url: GitHub comment URL where approval was given.

    Returns:
        The admin's @airbyte.io email address.

    Raises:
        GitHubCommentParseError: If the URL cannot be parsed.
        GitHubAPIError: If GitHub API calls fail.
        GitHubUserEmailNotFoundError: If the user has no public email or
            the email is not an @airbyte.io address.
    """
    owner, repo, comment_id, comment_type = _parse_github_comment_url(
        approval_comment_url
    )

    comment_info = get_github_comment_info(owner, repo, comment_id, comment_type)

    user_info = get_github_user_info(comment_info.author_login)

    if not user_info.email:
        raise GitHubUserEmailNotFoundError(
            f"GitHub user '{comment_info.author_login}' does not have a public email set. "
            f"To use this tool, the approver must have a public @airbyte.io email "
            f"configured on their GitHub profile (Settings > Public email)."
        )

    if not user_info.email.endswith("@airbyte.io"):
        raise GitHubUserEmailNotFoundError(
            f"GitHub user '{comment_info.author_login}' has public email '{user_info.email}' "
            f"which is not an @airbyte.io address. Only @airbyte.io emails are authorized "
            f"for admin operations."
        )

    return user_info.email
