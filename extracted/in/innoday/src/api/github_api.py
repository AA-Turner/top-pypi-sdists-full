"""GitHub API client for repository synchronization."""

import base64
import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import httpx

from src.api._base import BaseAPIClient
from src.utils.time_windows import parse_iso_naive

logger = logging.getLogger(__name__)

#: Pages of 100 commits `get_commits` will follow before it stops and says so.
#: Five is a deliberate ceiling, not a guess: 500 commits comfortably covers a
#: two-week window on this org's busiest repo, and an unbounded follow would let
#: one repo's history stall a synchronous summary read.
GITHUB_COMMITS_MAX_PAGES = 5


def _last_page(link_header: Optional[str]) -> Optional[int]:
    """The `page=` of the `rel="last"` link, or None when there is not one.

    GitHub omits the header entirely on a single-page result, which is why the
    caller falls back to counting the body rather than treating a missing header
    as zero.
    """
    if not link_header:
        return None
    for part in link_header.split(","):
        if 'rel="last"' not in part:
            continue
        match = re.search(r"[?&]page=(\d+)", part)
        if match:
            return int(match.group(1))
    return None


class GitHubAPIError(Exception):
    """A GitHub API call returned a non-success status.

    A typed error so callers can distinguish "GitHub said no" (bad/expired
    token, missing scope, org not visible) from a genuine internal fault. The
    former used to be raised as a bare `Exception`, which slipped past the
    routers' `except WorkspaceOnboardError` handlers and surfaced as an opaque
    500 — an expired token then looked like a server bug.
    """

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code

    @property
    def is_auth_error(self) -> bool:
        """401/403 — the credential is bad, revoked, or lacks the scope."""
        return self.status_code in (401, 403)


class GitHubAPI(BaseAPIClient):
    """API client for interacting with GitHub."""

    def __init__(
        self,
        token: Optional[str] = None,
        base_url: str = "https://api.github.com",
    ):
        # An `organization_alias` parameter used to be accepted here, resolving a
        # token from the CLI's config file plus the OS keyring when none was
        # passed. It was unreachable: every one of the ten construction sites
        # supplies an explicit token, and nothing anywhere passed the alias. On a
        # deployed server that lookup returns nothing silently, so the branch
        # could only ever have produced a confusing empty result -- see #525.
        self.base_url = base_url

        if not token:
            raise ValueError("GitHub token is required")

        self.token = token
        super().__init__(
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )

    async def validate_token(self) -> Dict[str, Any]:
        """Validate the GitHub token and get user information.

        Returns:
            Dict containing user information

        Raises:
            Exception: If token is invalid or API request fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/user", headers=self.headers)

            if response.status_code == 401:
                raise Exception("Invalid GitHub token")
            elif response.status_code != 200:
                raise Exception(f"Failed to validate token: {response.text}")

            return response.json()

    async def probe_token(self) -> Tuple[int, Optional[Dict[str, Any]]]:
        """Diagnostic sibling of ``validate_token``: report the status code.

        ``validate_token`` collapses every non-200 into a bare ``Exception``
        whose *message* is the only thing distinguishing them, so a caller
        cannot tell "GitHub rejected this token" (401/403) from "GitHub did not
        answer" (429, 5xx) without matching on text. A caller whose entire job
        is to report on a credential has to tell those apart: reporting a rate
        limit as an expired token is exactly the confident wrong answer
        ``validate_stored_github_credential`` exists to stop producing.

        Returns:
            ``(status_code, user_info)``. ``user_info`` is None for any non-200.

        Raises:
            Only what the transport raises -- unreachable host, TLS failure, a
            header value that cannot be encoded. **Those messages can quote the
            request, Authorization header included**, so a caller must never
            put the exception text in a response or a log line.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/user", headers=self.headers)

        if response.status_code != 200:
            return response.status_code, None
        return response.status_code, response.json()

    async def organization_access_status(self, org_name: str) -> int:
        """GitHub's status code for "can this token see this organization?".

        200 means yes. 401/403/404 are GitHub answering *no* (bad credential,
        missing scope, org not visible to it). Anything else -- 429, 5xx -- is
        GitHub not answering at all, which is not a verdict on the token.

        Args:
            org_name: GitHub organization name

        Returns:
            The HTTP status code of ``GET /orgs/{org_name}``
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/orgs/{org_name}", headers=self.headers
            )

        return response.status_code

    async def validate_organization_access(self, org_name: str) -> bool:
        """Check if the token has access to the specified organization.

        Collapses every non-200 to False, which is what the boolean callers
        want (``connect``, repository sync, repo refresh: no access and GitHub
        being down are both "cannot proceed"). A caller that must *report* on
        the credential rather than act on it wants
        ``organization_access_status`` instead.

        Args:
            org_name: GitHub organization name

        Returns:
            True if access is granted, False otherwise
        """
        return await self.organization_access_status(org_name) == 200

    async def get_organization_repositories(
        self, org_name: str, page: int = 1, per_page: int = 100
    ) -> List[Dict[str, Any]]:
        """Get all repositories for an organization.

        Args:
            org_name: GitHub organization name
            page: Page number for pagination
            per_page: Number of items per page (max 100)

        Returns:
            List of repository data dictionaries
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/orgs/{org_name}/repos",
                headers=self.headers,
                params={
                    "type": "all",
                    "sort": "updated",
                    "direction": "desc",
                    "page": page,
                    "per_page": per_page,
                },
            )

            if response.status_code != 200:
                raise GitHubAPIError(
                    f"Failed to fetch repositories for org '{org_name}' "
                    f"(HTTP {response.status_code}): {response.text}",
                    status_code=response.status_code,
                )

            return response.json()

    async def search_organization_repositories(
        self, org_name: str, topic: Optional[Union[str, Sequence[str]]] = None
    ) -> List[Dict[str, Any]]:
        """Search for repositories in an organization, optionally filtered by topic.

        Args:
            org_name: GitHub organization name
            topic: Optional topic, or several — a single string, a
                comma-separated string, or a sequence. A repo matching ANY of
                them is returned. None/empty means "every repo in the org".

        Returns:
            List of repository data dictionaries matching the criteria
        """
        # A project may span several topics (bp's BPAI repos carry both `bp-ai`
        # and `brightpower`). GitHub search has no topic-OR, so query each and
        # union the results, de-duplicating by repo id.
        parts = [topic] if isinstance(topic, str) else list(topic or [])
        topics = [
            t.strip().lower()
            for part in parts
            for t in str(part).split(",")
            if t.strip()
        ]

        if not topics:
            # Fall back to getting all repositories
            return await self.get_all_organization_repositories(org_name)

        found: Dict[int, Dict[str, Any]] = {}
        async with httpx.AsyncClient() as client:
            for one_topic in topics:
                search_query = f"org:{org_name} topic:{one_topic}"
                page = 1
                while True:
                    # Paginate: search used to request a single page of 100 and
                    # stop. Callers treat "absent from the results" as "lost the
                    # topic" and deactivate the link, so a silent truncation at
                    # 100 would soft-delete real repos.
                    response = await client.get(
                        f"{self.base_url}/search/repositories",
                        headers=self.headers,
                        params={"q": search_query, "per_page": 100, "page": page},
                    )

                    if response.status_code != 200:
                        raise GitHubAPIError(
                            f"Search failed for topic '{one_topic}' in org "
                            f"'{org_name}' (HTTP {response.status_code}): "
                            f"{response.text}",
                            status_code=response.status_code,
                        )

                    items = response.json().get("items", [])
                    for item in items:
                        found[item["id"]] = item
                    if len(items) < 100:
                        break
                    page += 1

        return list(found.values())

    async def get_all_organization_repositories(
        self, org_name: str
    ) -> List[Dict[str, Any]]:
        """Get all repositories for an organization with pagination.

        Args:
            org_name: GitHub organization name

        Returns:
            List of all repository data dictionaries
        """
        all_repos = []
        page = 1

        while True:
            repos = await self.get_organization_repositories(org_name, page=page)
            if not repos:
                break

            all_repos.extend(repos)

            # GitHub API returns empty list when no more pages
            if len(repos) < 100:
                break

            page += 1

        return all_repos

    async def get_repository_readme(
        self, owner: str, repo: str, ref: Optional[str] = None
    ) -> Optional[str]:
        """Get the README content for a repository.

        Args:
            owner: Repository owner (user or organization)
            repo: Repository name
            ref: Git reference (branch, tag, commit SHA) - defaults to default branch

        Returns:
            README content as string, or None if not found
        """
        async with httpx.AsyncClient() as client:
            params = {}
            if ref:
                params["ref"] = ref

            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/readme",
                headers=self.headers,
                params=params,
            )

            if response.status_code == 404:
                # No README found
                return None
            elif response.status_code != 200:
                raise Exception(f"Failed to fetch README: {response.text}")

            data = response.json()

            # README content is base64 encoded
            if data.get("encoding") == "base64" and data.get("content"):
                content = base64.b64decode(data["content"]).decode("utf-8")
                return content

            return None

    async def get_repository_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """Get programming languages used in a repository.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Dict mapping language names to bytes of code
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/languages", headers=self.headers
            )

            if response.status_code != 200:
                return {}

            return response.json()

    def parse_repository_data(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse GitHub repository data into a format suitable for Repository model.

        Args:
            repo_data: Raw repository data from GitHub API

        Returns:
            Dict with parsed repository fields
        """
        return {
            "id": str(repo_data["id"]),
            "name": repo_data["name"],
            "full_name": repo_data["full_name"],
            "url": repo_data["html_url"],
            "description": repo_data.get("description"),
            "language": repo_data.get("language"),
            "stars": repo_data.get("stargazers_count", 0),
            "forks": repo_data.get("forks_count", 0),
            "open_issues_count": repo_data.get("open_issues_count", 0),
            "is_private": repo_data.get("private", False),
            "archived": repo_data.get("archived", False),
            # `parse_iso_naive`: the columns are naive, and these parse a
            # third-party payload -- an unexpected shape from GitHub should cost
            # one null field, not raise partway through building a repo record.
            # The previous form also indexed `repo_data["created_at"]` after a
            # `.get()` guard, so a truthy-but-absent race was a KeyError.
            "github_created_at": parse_iso_naive(repo_data.get("created_at")),
            "github_updated_at": parse_iso_naive(repo_data.get("updated_at")),
        }

    async def get_rate_limit(self) -> Dict[str, Any]:
        """Get current API rate limit status.

        Returns:
            Dict containing rate limit information
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/rate_limit", headers=self.headers
            )

            if response.status_code != 200:
                raise Exception(f"Failed to get rate limit: {response.text}")

            return response.json()

    async def get_repository_topics(self, owner: str, repo: str) -> List[str]:
        """Get the current GitHub topics for a repository.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            List of topic strings
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/topics",
                headers={
                    **self.headers,
                    "Accept": "application/vnd.github.mercy-preview+json",
                },
            )

            if response.status_code != 200:
                raise Exception(f"Failed to get repository topics: {response.text}")

            return response.json().get("names", [])

    async def set_repository_topics(
        self, owner: str, repo: str, topics: List[str]
    ) -> List[str]:
        """Replace all topics on a repository (GitHub's topics endpoint is a
        full-replace PUT, not add/remove -- callers must GET current topics,
        mutate the set, and pass the full result here to avoid clobbering
        unrelated topics the repo already carries.

        Args:
            owner: Repository owner
            repo: Repository name
            topics: The complete new set of topics

        Returns:
            The resulting list of topic strings
        """
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}/repos/{owner}/{repo}/topics",
                headers={
                    **self.headers,
                    "Accept": "application/vnd.github.mercy-preview+json",
                },
                json={"names": topics},
            )

            if response.status_code != 200:
                raise Exception(f"Failed to set repository topics: {response.text}")

            return response.json().get("names", [])

    async def add_repository_topic(
        self, owner: str, repo: str, topic: str
    ) -> List[str]:
        """Add a single topic to a repository without disturbing existing topics.

        Note: GitHub's topics API has no ETag/If-Match support, so this
        get-then-put is not atomic -- two concurrent callers mutating the
        same repo's topics can race, and whichever PUT lands second wins,
        silently discarding the other's change. Acceptable here because the
        only caller (project repo sync/removal) only touches InnoDay's own
        DB state after this call succeeds, so the failure mode is a wrong
        topic label on GitHub, not corrupted InnoDay data -- a re-sync
        corrects it. Worth revisiting if a second concurrent topic-mutating
        caller is ever added.
        """
        current = await self.get_repository_topics(owner, repo)
        if topic in current:
            return current
        return await self.set_repository_topics(owner, repo, current + [topic])

    async def remove_repository_topic(
        self, owner: str, repo: str, topic: str
    ) -> List[str]:
        """Remove a single topic from a repository without disturbing others."""
        current = await self.get_repository_topics(owner, repo)
        if topic not in current:
            return current
        return await self.set_repository_topics(
            owner, repo, [t for t in current if t != topic]
        )

    async def get_repository(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """Get repository information.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Repository data or None if not found
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}", headers=self.headers
            )

            if response.status_code == 404:
                return None
            elif response.status_code != 200:
                raise Exception(f"Failed to get repository: {response.text}")

            return response.json()

    async def get_issues(
        self,
        owner: str,
        repo: str,
        state: str = "all",
        since: Optional[datetime] = None,
        page: int = 1,
        per_page: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get issues for a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            state: Issue state (open, closed, all)
            since: Only issues updated after this time
            page: Page number for pagination
            per_page: Number of items per page

        Returns:
            List of issue dictionaries
        """
        params = {
            "state": state,
            "page": page,
            "per_page": per_page,
            "sort": "updated",
            "direction": "desc",
        }

        if since:
            params["since"] = since.isoformat() + "Z"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/issues",
                headers=self.headers,
                params=params,
            )

            if response.status_code != 200:
                raise Exception(f"Failed to get issues: {response.text}")

            return response.json()

    async def get_pull_requests(
        self,
        owner: str,
        repo: str,
        state: str = "all",
        since: Optional[datetime] = None,
        page: int = 1,
        per_page: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get pull requests for a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            state: PR state (open, closed, all)
            since: Only PRs updated after this time
            page: Page number for pagination
            per_page: Number of items per page

        Returns:
            List of pull request dictionaries
        """
        params = {
            "state": state,
            "page": page,
            "per_page": per_page,
            "sort": "updated",
            "direction": "desc",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/pulls",
                headers=self.headers,
                params=params,
            )

            if response.status_code != 200:
                raise Exception(f"Failed to get pull requests: {response.text}")

            # Filter by updated date if provided
            pulls = response.json()
            if since:
                since_str = since.isoformat() + "Z"
                pulls = [pr for pr in pulls if pr.get("updated_at", "") >= since_str]

            return pulls

    async def list_pull_requests(
        self,
        owner: str,
        repo: str,
        state: str = "all",
        since: Optional[datetime] = None,
        max_pages: int = 10,
    ) -> Tuple[List[Dict[str, Any]], bool]:
        """Every pull request in the window, across pages, and whether that is all.

        `get_pull_requests` fetches **one page of a hundred**, sorted by most
        recently updated. On a quiet repository that is the whole answer, so the
        limit was invisible; on a busy one the hundred-and-first pull request
        simply did not exist, in the very report whose job is to say what a
        release contains. Silent truncation reads exactly like coverage.

        Two things make paging cheap here. Results come back newest-updated
        first, so once a page ends older than `since` nothing beyond it can be in
        the window and we stop. And a pull request merged inside the window was
        necessarily *updated* inside it too, so that early exit cannot drop a
        merged one.

        Returns `(pull_requests, truncated)`. `truncated` is True only when
        `max_pages` ran out with more still to come -- the caller is expected to
        say so rather than present a short list as the complete one.
        """
        collected: List[Dict[str, Any]] = []
        since_str = (since.isoformat() + "Z") if since else None

        for page in range(1, max_pages + 1):
            batch = await self.get_pull_requests(
                owner, repo, state=state, since=None, page=page, per_page=100
            )
            if not batch:
                return collected, False

            if since_str is not None:
                collected.extend(
                    pr for pr in batch if (pr.get("updated_at") or "") >= since_str
                )
                # Sorted newest-updated first, so a page whose last entry is
                # older than the window means every later page is too.
                if (batch[-1].get("updated_at") or "") < since_str:
                    return collected, False
            else:
                collected.extend(batch)

            if len(batch) < 100:
                return collected, False

        return collected, True

    async def pull_request_commits(
        self, owner: str, repo: str, number: int
    ) -> List[str]:
        """The commit subjects on one pull request, for proposing a match.

        A pull request that names no ticket in its branch, title or description
        still says what it did, and it says it most plainly here: "rename
        Estimated Cost to Cost" is recognisably a checklist item on a ticket
        nobody linked.

        Fetched only for the pull requests that matched nothing, so the cost is
        bounded by the size of the problem rather than the size of the release.
        Subjects only -- a full commit is a diff, and nothing here reads diffs.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/pulls/{number}/commits",
                headers=self.headers,
                params={"per_page": 100},
            )
        if response.status_code != 200:
            return []
        body = response.json()
        if not isinstance(body, list):
            return []
        return [
            ((c.get("commit") or {}).get("message") or "").splitlines()[0]
            for c in body
            if ((c.get("commit") or {}).get("message") or "").strip()
        ]

    async def count_commits(
        self,
        owner: str,
        repo: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        sha: Optional[str] = None,
    ) -> int:
        """How many commits are in the window, in **one** request.

        `get_commits` pages through the window a hundred at a time, up to five
        times, and a caller that only wants a number was downloading as many as
        five hundred commit objects per repository to call `len()` on them. On a
        seven-repository release that was most of a seventeen-second wait.

        With `per_page=1`, GitHub's `Link` header names the last page — and one
        commit per page means the last page number *is* the count. No commit
        bodies come back at all.

        Same 404/409 handling as `get_commits`: an empty repository, or a branch
        that does not exist, means "no commits", not a fault.
        """
        params: Dict[str, Any] = {"per_page": 1}
        if since is not None:
            params["since"] = since.isoformat()
        if until is not None:
            params["until"] = until.isoformat()
        if sha:
            params["sha"] = sha

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/commits",
                headers=self.headers,
                params=params,
            )
        if response.status_code in (404, 409):
            return 0
        if response.status_code != 200:
            raise GitHubAPIError(
                f"Failed to count commits for {owner}/{repo}: {response.text}",
                status_code=response.status_code,
            )

        last = _last_page(response.headers.get("Link"))
        if last is not None:
            return last
        # No Link header means a single page, so the body is the whole answer:
        # one commit, or none at all.
        body = response.json()
        return len(body) if isinstance(body, list) else 0

    async def get_commits(
        self,
        owner: str,
        repo: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        sha: Optional[str] = None,
        per_page: int = 100,
        max_pages: int = GITHUB_COMMITS_MAX_PAGES,
    ) -> List[Dict[str, Any]]:
        """Commits on a branch, bounded by a time window.

        `since`/`until` are passed to GitHub rather than filtered here: the
        window is the whole point of the call and letting the server bound it
        does most of the narrowing.

        **Paginated, with an explicit ceiling.** A single `per_page=100` request
        silently truncated a busy repo's two-week window at 100 commits and
        reported the remainder as "nothing happened" -- a wrong answer that
        looks exactly like a right one. Pages are followed to `max_pages`
        (`GITHUB_COMMITS_MAX_PAGES`) and the truncation is logged, so the limit
        is a stated bound rather than an accident.

        A repo that is empty, or whose branch does not exist, answers 404/409.
        Both mean "no commits to report", not a fault, so both return `[]` --
        a summary must not fail because one repo in the project is a stub.
        """
        base_params: Dict[str, Any] = {"per_page": per_page}
        if since is not None:
            base_params["since"] = since.isoformat()
        if until is not None:
            base_params["until"] = until.isoformat()
        if sha:
            base_params["sha"] = sha

        commits: List[Dict[str, Any]] = []
        async with httpx.AsyncClient() as client:
            for page in range(1, max(1, max_pages) + 1):
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/commits",
                    headers=self.headers,
                    params={**base_params, "page": page},
                )
                if response.status_code in (404, 409):
                    return []
                if response.status_code != 200:
                    raise GitHubAPIError(
                        f"Failed to get commits for {owner}/{repo}: {response.text}",
                        status_code=response.status_code,
                    )
                data = response.json()
                if not isinstance(data, list) or not data:
                    break
                commits.extend(data)
                if len(data) < per_page:
                    break
            else:
                logger.warning(
                    "Commit history for %s/%s truncated at %d commits (%d pages) "
                    "-- the window holds more than this call reports",
                    owner,
                    repo,
                    len(commits),
                    max_pages,
                )
        return commits

    async def get_releases(
        self, owner: str, repo: str, per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """Published GitHub releases for a repository, newest first.

        Releases, not tags: blastoff creates a GitHub Release per version, and a
        release carries the publication timestamp and draft/prerelease flags that
        a bare tag does not. A repo with tags but no releases returns [] rather
        than guessing -- an untagged-but-released repo is a release-process
        problem, not something to infer here.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/releases",
                headers=self.headers,
                params={"per_page": per_page},
            )
            # 404 is normal: a repo may simply have no releases, and many do not.
            if response.status_code == 404:
                return []
            if response.status_code != 200:
                raise Exception(f"Failed to get releases: {response.text}")
            data = response.json()
        return data if isinstance(data, list) else []

    async def list_open_pull_requests(
        self, owner: str, repo: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Every open pull request on a repository, or ``None`` if unreadable.

        ``None`` rather than ``[]`` on failure, so a repo whose PRs could not be
        fetched is not indistinguishable from one with nothing open. That
        distinction is the whole reason this is kept separately from GitHub's
        `open_issues_count`, which lumps issues and PRs together -- and it is why
        the caller must not delete stored rows when this returns ``None``.

        This used to be ``count_open_pull_requests``, which made exactly this
        request and then returned ``len(prs)``, discarding the title, number,
        url, author, assignees and draft state (#500). The count is now derived
        from what is kept, so the two cannot disagree.
        """
        try:
            prs = await self.get_pull_requests(owner, repo, state="open", per_page=100)
        except Exception:  # noqa: BLE001 - PRs are never worth failing a sync
            return None
        return prs if isinstance(prs, list) else None

    async def get_pull_request_outcome(
        self, owner: str, repo: str, number: int
    ) -> Optional[Dict[str, Any]]:
        """How one pull request ended: ``{"state", "merged_at"}``, or ``None``.

        ``None`` means *unanswered* -- a 404, a network failure, any non-200 --
        and the caller must not read it as either outcome.

        Separate from :meth:`get_pull_request_state` rather than widening it.
        That one is deliberately narrowed to the state string because its single
        job is "is this still open", and its docstring warns against handing back
        a payload people would find a second use for. This has a different
        question: a pull request that left the open list either **merged** or was
        **abandoned**, and only the first shipped anything. Two callers, two
        questions, two methods that cannot drift into each other.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/pulls/{number}",
                    headers=self.headers,
                )
        except Exception:  # noqa: BLE001 - an unanswered probe is not an outcome
            return None
        if response.status_code != 200:
            return None
        try:
            pr = response.json()
        except Exception:  # noqa: BLE001 - a body that will not parse said nothing
            return None
        if not isinstance(pr, dict):
            return None
        return {"state": pr.get("state"), "merged_at": pr.get("merged_at")}

    async def get_pull_request_state(
        self, owner: str, repo: str, number: int
    ) -> Optional[str]:
        """One pull request's state -- ``"open"``, ``"closed"``, or ``None``.

        ``None`` means *unanswered*, not "no such PR": a 404, a network failure or
        any non-200. The caller must not read it as either state.

        This exists so that ``list_open_pull_requests`` returning ``[]`` can be
        checked rather than believed. An empty list is what a repository with
        nothing open returns **and** what a token that has quietly lost access to
        the repository returns -- both HTTP 200, both `[]`. Asking about one
        specific pull request the caller already has on file separates them: a
        token that cannot see the repo cannot answer this either, and a pull
        request that is genuinely still open says so. See
        ``GitHubConnectService._empty_pr_list_is_believable``.

        Deliberately narrowed to the state string rather than returning the
        payload. The only question is "is this one still open"; handing back the
        whole object would invite a second, unvalidated use of a single-PR fetch
        that the empty-list check pays for.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/pulls/{number}",
                    headers=self.headers,
                )
        except Exception:  # noqa: BLE001 - an unanswered probe is not a state
            return None
        if response.status_code != 200:
            return None
        try:
            state = response.json().get("state")
        except Exception:  # noqa: BLE001 - a body that will not parse said nothing
            return None
        return state if isinstance(state, str) else None

    async def get_organization_repos(self, org_name: str) -> List[Dict[str, Any]]:
        """Get all repositories for an organization.

        This is an alias for get_all_organization_repositories for consistency
        with the API endpoint naming.

        Args:
            org_name: GitHub organization name

        Returns:
            List of repository dictionaries
        """
        return await self.get_all_organization_repositories(org_name)
