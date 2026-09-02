"""GitHub Issues API client for repository issue synchronization."""

import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Optional

import httpx
from pydantic import BaseModel


class GitHubRateLimit(BaseModel):
    """GitHub API rate limit information"""

    limit: int
    remaining: int
    reset: int
    used: int


class GitHubIssuesAPI:
    """GitHub API client for issue synchronization"""

    def __init__(self, token: str, base_url: str = "https://api.github.com"):
        """
        Initialize GitHub Issues API client

        Args:
            token: GitHub personal access token
            base_url: GitHub API base URL (for GitHub Enterprise)
        """
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.session: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "InnoDay-GitHub-Issues-Sync/1.0",
            },
            timeout=30.0,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.aclose()
            self.session = None

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make authenticated request to GitHub API"""
        if not self.session:
            raise RuntimeError("GitHubIssuesAPI must be used as async context manager")

        url = f"{self.base_url}{endpoint}"

        try:
            response = await self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ValueError("Invalid GitHub token or insufficient permissions")
            elif e.response.status_code == 403:
                # Check if it's rate limiting
                if "rate limit" in e.response.text.lower():
                    rate_limit = await self.get_rate_limit()
                    raise ValueError(
                        f"GitHub API rate limit exceeded. Resets at {rate_limit.reset}"
                    )
                raise ValueError(f"GitHub API access forbidden: {e.response.text}")
            elif e.response.status_code == 404:
                raise ValueError("Repository not found or no access")
            else:
                raise ValueError(
                    f"GitHub API error {e.response.status_code}: {e.response.text}"
                )
        except httpx.RequestError as e:
            raise ValueError(f"GitHub API request failed: {str(e)}")

    async def get_rate_limit(self) -> GitHubRateLimit:
        """Get current GitHub API rate limit status"""
        data = await self._request("GET", "/rate_limit")
        core = data["resources"]["core"]
        return GitHubRateLimit(**core)

    async def test_connection(self) -> Dict[str, str]:
        """Test GitHub API connection and return user info"""
        try:
            user_data = await self._request("GET", "/user")
            return {
                "status": "success",
                "user": user_data.get("login", "unknown"),
                "name": user_data.get("name", ""),
                "message": f"Connected as {user_data.get('login', 'unknown')}",
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def get_repository_info(self, owner: str, repo: str) -> Dict:
        """Get basic repository information"""
        return await self._request("GET", f"/repos/{owner}/{repo}")

    async def get_repository_issues(
        self,
        owner: str,
        repo: str,
        state: str = "all",
        since: Optional[datetime] = None,
        page: int = 1,
        per_page: int = 100,
    ) -> List[Dict]:
        """
        Fetch issues from a GitHub repository

        Args:
            owner: Repository owner (user or organization)
            repo: Repository name
            state: Issue state filter ("open", "closed", "all")
            since: Only issues updated after this date
            page: Page number for pagination
            per_page: Number of issues per page (max 100)

        Returns:
            List of GitHub issue dictionaries
        """
        params = {
            "state": state,
            "page": page,
            "per_page": min(per_page, 100),  # GitHub API limit
            "sort": "updated",
            "direction": "desc",
        }

        if since:
            params["since"] = since.isoformat()

        return await self._request(
            "GET", f"/repos/{owner}/{repo}/issues", params=params
        )

    async def get_all_repository_issues(
        self,
        owner: str,
        repo: str,
        state: str = "all",
        since: Optional[datetime] = None,
        max_pages: int = 50,
    ) -> List[Dict]:
        """
        Fetch all issues from a repository with automatic pagination

        Args:
            owner: Repository owner
            repo: Repository name
            state: Issue state filter
            since: Only issues updated after this date
            max_pages: Maximum pages to fetch (safety limit)

        Returns:
            Complete list of GitHub issues
        """
        all_issues = []
        page = 1

        while page <= max_pages:
            issues = await self.get_repository_issues(
                owner, repo, state=state, since=since, page=page, per_page=100
            )

            if not issues:
                break  # No more issues

            all_issues.extend(issues)

            # If we got less than 100 issues, we've reached the end
            if len(issues) < 100:
                break

            page += 1

            # Be nice to GitHub API - small delay between requests
            await asyncio.sleep(0.1)

        return all_issues

    async def get_issue_details(self, owner: str, repo: str, issue_number: int) -> Dict:
        """
        Get detailed information for a specific issue

        Args:
            owner: Repository owner
            repo: Repository name
            issue_number: GitHub issue number

        Returns:
            Detailed issue information
        """
        return await self._request(
            "GET", f"/repos/{owner}/{repo}/issues/{issue_number}"
        )

    async def validate_repository_access(self, owner: str, repo: str) -> bool:
        """
        Validate that the current token has access to the repository

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            True if access is valid, False otherwise
        """
        try:
            await self.get_repository_info(owner, repo)
            return True
        except ValueError as e:
            if "not found" in str(e).lower() or "no access" in str(e).lower():
                return False
            raise  # Re-raise other errors

    def parse_repository_url(self, url: str) -> Optional[tuple[str, str]]:
        """
        Parse GitHub repository URL to extract owner and repo name

        Args:
            url: GitHub repository URL

        Returns:
            Tuple of (owner, repo) or None if invalid
        """
        import re

        # Support various GitHub URL formats
        patterns = [
            r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?/?$",
            r"github\.com/([^/]+)/([^/]+)/?$",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                owner, repo = match.groups()
                # Remove .git suffix if present
                if repo.endswith(".git"):
                    repo = repo[:-4]
                return owner, repo

        return None


class GitHubIssuesSyncStats(BaseModel):
    """Statistics from a GitHub issues sync operation"""

    total_fetched: int = 0
    issues_created: int = 0
    issues_updated: int = 0
    issues_skipped: int = 0
    errors: List[str] = []
    started_at: datetime
    completed_at: Optional[datetime] = None

    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate sync duration in seconds"""
        if self.completed_at and self.started_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    def mark_completed(self) -> None:
        """Mark the sync operation as completed"""
        self.completed_at = datetime.now(timezone.utc)

    def add_error(self, error: str) -> None:
        """Add an error message to the sync stats"""
        self.errors.append(error)
