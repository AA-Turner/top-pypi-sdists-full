"""GitHub MCP tools for live GitHub integration.

These tools use the GitHub MCP server to provide real-time
GitHub functionality including code search, PR analysis, and more.
"""

import json
from typing import Any, Optional

from .base import BaseTool, ToolResult, ToolCategory
from ...utils.logger import log


class MCPBaseTool(BaseTool):
    """Base class for MCP-backed tools."""

    category = ToolCategory.HISTORY

    def _get_mcp_client(self):
        """Get the MCP client, starting if needed.

        Returns:
            GitHubMCPClient instance or None
        """
        try:
            from ..mcp.client import GitHubMCPClient

            client = GitHubMCPClient()
            if not client.is_running:
                client.start()
            return client
        except Exception as e:
            log.warning(f"Failed to get MCP client: {e}")
            return None

    def _call_mcp_tool(
        self,
        tool_name: str,
        arguments: dict,
    ) -> ToolResult:
        """Call an MCP tool and return result.

        Args:
            tool_name: MCP tool name
            arguments: Tool arguments

        Returns:
            ToolResult
        """
        client = self._get_mcp_client()
        if not client:
            return ToolResult.error_result(
                "GitHub MCP not available",
                suggestions=["Check GITHUB_TOKEN is set", "Install github-mcp-server"],
            )

        try:
            response = client.call_tool(tool_name, arguments)

            if response.is_error:
                return ToolResult.error_result(response.get_text())

            # Parse response content
            result_data = {"raw": response.get_text()}

            # Try to parse as JSON
            for item in response.content:
                if item.get("type") == "text":
                    try:
                        parsed = json.loads(item.get("text", ""))
                        if isinstance(parsed, dict):
                            result_data.update(parsed)
                        elif isinstance(parsed, list):
                            result_data["results"] = parsed
                    except json.JSONDecodeError:
                        pass

            return ToolResult.success_result(data=result_data)

        except Exception as e:
            log.exception(f"MCP tool call failed: {tool_name}")
            return ToolResult.error_result(f"MCP call failed: {str(e)}")


class GitHubSearchCodeTool(MCPBaseTool):
    """Search code on GitHub."""

    name = "github_search_code"
    description = """Search for code across GitHub repositories.
Finds code matching a query, useful for finding implementations,
patterns, or usage examples."""

    def execute(
        self,
        query: str,
        repo: Optional[str] = None,
        language: Optional[str] = None,
        per_page: int = 10,
    ) -> ToolResult:
        """Search GitHub code.

        Args:
            query: Search query
            repo: Optional repo filter (owner/repo)
            language: Optional language filter
            per_page: Results per page

        Returns:
            ToolResult with code matches
        """
        full_query = query
        if repo:
            full_query += f" repo:{repo}"
        if language:
            full_query += f" language:{language}"

        return self._call_mcp_tool("search_code", {
            "query": full_query,
            "per_page": per_page,
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "query": {
                    "type": "string",
                    "description": "Search query for code",
                },
                "repo": {
                    "type": "string",
                    "description": "Repository filter (owner/repo)",
                },
                "language": {
                    "type": "string",
                    "description": "Language filter",
                },
                "per_page": {
                    "type": "integer",
                    "description": "Results per page",
                    "default": 10,
                },
            },
            required=["query"],
        )


class GitHubGetFileContentTool(MCPBaseTool):
    """Get file content from GitHub."""

    name = "github_get_file_content"
    description = """Get the content of a file from a GitHub repository.
Retrieves the actual file content for analysis."""

    def execute(
        self,
        owner: str,
        repo: str,
        path: str,
        ref: Optional[str] = None,
    ) -> ToolResult:
        """Get file content.

        Args:
            owner: Repository owner
            repo: Repository name
            path: File path
            ref: Optional git ref (branch, tag, commit)

        Returns:
            ToolResult with file content
        """
        args = {"owner": owner, "repo": repo, "path": path}
        if ref:
            args["ref"] = ref

        return self._call_mcp_tool("get_file_contents", args)

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "owner": {
                    "type": "string",
                    "description": "Repository owner",
                },
                "repo": {
                    "type": "string",
                    "description": "Repository name",
                },
                "path": {
                    "type": "string",
                    "description": "Path to the file",
                },
                "ref": {
                    "type": "string",
                    "description": "Git reference (branch, tag, commit)",
                },
            },
            required=["owner", "repo", "path"],
        )


class GitHubPRDetailsTool(MCPBaseTool):
    """Get detailed PR information."""

    name = "github_pr_details"
    description = """Get detailed information about a pull request.
Includes diff, comments, reviews, and status."""

    def execute(
        self,
        owner: str,
        repo: str,
        pull_number: int,
    ) -> ToolResult:
        """Get PR details.

        Args:
            owner: Repository owner
            repo: Repository name
            pull_number: PR number

        Returns:
            ToolResult with PR details
        """
        return self._call_mcp_tool("get_pull_request", {
            "owner": owner,
            "repo": repo,
            "pull_number": pull_number,
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "owner": {
                    "type": "string",
                    "description": "Repository owner",
                },
                "repo": {
                    "type": "string",
                    "description": "Repository name",
                },
                "pull_number": {
                    "type": "integer",
                    "description": "Pull request number",
                },
            },
            required=["owner", "repo", "pull_number"],
        )


class GitHubListPRsTool(MCPBaseTool):
    """List pull requests."""

    name = "github_list_prs"
    description = """List pull requests for a repository.
Can filter by state (open, closed, all)."""

    def execute(
        self,
        owner: str,
        repo: str,
        state: str = "open",
        per_page: int = 10,
    ) -> ToolResult:
        """List PRs.

        Args:
            owner: Repository owner
            repo: Repository name
            state: PR state filter (open, closed, all)
            per_page: Results per page

        Returns:
            ToolResult with PR list
        """
        return self._call_mcp_tool("list_pull_requests", {
            "owner": owner,
            "repo": repo,
            "state": state,
            "per_page": per_page,
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "owner": {
                    "type": "string",
                    "description": "Repository owner",
                },
                "repo": {
                    "type": "string",
                    "description": "Repository name",
                },
                "state": {
                    "type": "string",
                    "enum": ["open", "closed", "all"],
                    "description": "PR state filter",
                    "default": "open",
                },
                "per_page": {
                    "type": "integer",
                    "description": "Results per page",
                    "default": 10,
                },
            },
            required=["owner", "repo"],
        )


class GitHubSearchReposTool(MCPBaseTool):
    """Search GitHub repositories."""

    name = "github_search_repos"
    description = """Search for repositories on GitHub.
Find repos by topic, name, or description."""

    def execute(
        self,
        query: str,
        per_page: int = 10,
    ) -> ToolResult:
        """Search repositories.

        Args:
            query: Search query
            per_page: Results per page

        Returns:
            ToolResult with repo matches
        """
        return self._call_mcp_tool("search_repositories", {
            "query": query,
            "per_page": per_page,
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "query": {
                    "type": "string",
                    "description": "Search query",
                },
                "per_page": {
                    "type": "integer",
                    "description": "Results per page",
                    "default": 10,
                },
            },
            required=["query"],
        )


class GitHubSearchPRsTool(MCPBaseTool):
    """Search pull requests on GitHub."""

    name = "github_search_prs"
    description = """Search for pull requests across GitHub.
Find PRs by title, body, or comments."""

    def execute(
        self,
        query: str,
        repo: Optional[str] = None,
        state: Optional[str] = None,
        per_page: int = 10,
    ) -> ToolResult:
        """Search PRs.

        Args:
            query: Search query
            repo: Optional repo filter
            state: Optional state filter
            per_page: Results per page

        Returns:
            ToolResult with PR matches
        """
        full_query = query + " is:pr"
        if repo:
            full_query += f" repo:{repo}"
        if state:
            full_query += f" is:{state}"

        return self._call_mcp_tool("search_issues", {
            "query": full_query,
            "per_page": per_page,
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "query": {
                    "type": "string",
                    "description": "Search query",
                },
                "repo": {
                    "type": "string",
                    "description": "Repository filter (owner/repo)",
                },
                "state": {
                    "type": "string",
                    "enum": ["open", "closed"],
                    "description": "PR state filter",
                },
                "per_page": {
                    "type": "integer",
                    "description": "Results per page",
                    "default": 10,
                },
            },
            required=["query"],
        )


class GitHubGetIssueTool(MCPBaseTool):
    """Get issue details from GitHub."""

    name = "github_get_issue"
    description = """Get detailed information about an issue.
Includes body, comments, labels, and assignees."""

    def execute(
        self,
        owner: str,
        repo: str,
        issue_number: int,
    ) -> ToolResult:
        """Get issue details.

        Args:
            owner: Repository owner
            repo: Repository name
            issue_number: Issue number

        Returns:
            ToolResult with issue details
        """
        return self._call_mcp_tool("get_issue", {
            "owner": owner,
            "repo": repo,
            "issue_number": issue_number,
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "owner": {
                    "type": "string",
                    "description": "Repository owner",
                },
                "repo": {
                    "type": "string",
                    "description": "Repository name",
                },
                "issue_number": {
                    "type": "integer",
                    "description": "Issue number",
                },
            },
            required=["owner", "repo", "issue_number"],
        )


class GitHubViewRepoStructureTool(MCPBaseTool):
    """View repository structure."""

    name = "github_view_repo_structure"
    description = """View the directory structure of a GitHub repository.
Shows files and folders in a tree format."""

    def execute(
        self,
        owner: str,
        repo: str,
        path: str = "",
        ref: Optional[str] = None,
    ) -> ToolResult:
        """View repo structure.

        Args:
            owner: Repository owner
            repo: Repository name
            path: Path within repo
            ref: Git reference

        Returns:
            ToolResult with directory structure
        """
        args = {"owner": owner, "repo": repo}
        if path:
            args["path"] = path
        if ref:
            args["ref"] = ref

        return self._call_mcp_tool("get_directory_contents", args)

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "owner": {
                    "type": "string",
                    "description": "Repository owner",
                },
                "repo": {
                    "type": "string",
                    "description": "Repository name",
                },
                "path": {
                    "type": "string",
                    "description": "Path within the repository",
                    "default": "",
                },
                "ref": {
                    "type": "string",
                    "description": "Git reference (branch, tag, commit)",
                },
            },
            required=["owner", "repo"],
        )


class GitHubCreateReviewTool(MCPBaseTool):
    """Create a PR review."""

    name = "github_create_review"
    description = """Create a review on a pull request.
Can approve, request changes, or comment."""

    def execute(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        event: str,
        body: str,
    ) -> ToolResult:
        """Create a review.

        Args:
            owner: Repository owner
            repo: Repository name
            pull_number: PR number
            event: Review event (APPROVE, REQUEST_CHANGES, COMMENT)
            body: Review body

        Returns:
            ToolResult with review details
        """
        return self._call_mcp_tool("create_pull_request_review", {
            "owner": owner,
            "repo": repo,
            "pull_number": pull_number,
            "event": event,
            "body": body,
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "owner": {
                    "type": "string",
                    "description": "Repository owner",
                },
                "repo": {
                    "type": "string",
                    "description": "Repository name",
                },
                "pull_number": {
                    "type": "integer",
                    "description": "Pull request number",
                },
                "event": {
                    "type": "string",
                    "enum": ["APPROVE", "REQUEST_CHANGES", "COMMENT"],
                    "description": "Review event type",
                },
                "body": {
                    "type": "string",
                    "description": "Review body/comment",
                },
            },
            required=["owner", "repo", "pull_number", "event", "body"],
        )
