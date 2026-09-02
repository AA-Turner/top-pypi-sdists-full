"""Built-in tool registrations (FR-009).

Registers 20+ tools across 7 categories (git, jira, azure_devops,
github, filesystem, testing, state) into a ``ConcreteToolRegistry``.
Config is injected at construction time via closures.
"""

from __future__ import annotations

import contextlib
import functools
import io
import logging
import pathlib
import re
import subprocess
import sys
from typing import Any

from .definition import ToolDefinition
from .registry import ConcreteToolRegistry

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Filesystem containment helpers
# ---------------------------------------------------------------------------


@functools.lru_cache(maxsize=1)
def _get_cached_git_root() -> pathlib.Path | None:
    """Resolve and cache the repository root from git, if available."""
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return pathlib.Path(proc.stdout.strip()).resolve()
    except Exception:  # noqa: BLE001
        logger.debug(
            "Failed to determine git root for filesystem containment",
            exc_info=True,
        )
    return None


def _get_allowed_roots() -> list[pathlib.Path]:
    """Return the set of filesystem roots that tool operations may access.

    Priority:
    1. Git repository root (``git rev-parse --show-toplevel``), cached.
    2. The AGDT state directory (appended when it falls outside the repo).

    Returns an **empty list** when both sources are unavailable, which
    causes all filesystem-containment checks to deny access (fail-closed).
    Falling back to the process CWD is intentionally avoided because it
    would grant an LLM-driven tool read/write access to an arbitrary host
    directory tree.

    The returned paths are fully resolved (symlinks expanded).
    """
    roots: list[pathlib.Path] = []
    git_root = _get_cached_git_root()
    if git_root is not None:
        roots.append(git_root)

    state_dir: pathlib.Path | None = None
    try:
        from agentic_devtools.state import get_state_dir

        state_dir = pathlib.Path(get_state_dir()).resolve()
    except Exception:  # noqa: BLE001
        logger.debug(
            "Failed to resolve AGDT state dir for filesystem allowed roots",
            exc_info=True,
        )

    if state_dir is not None and not any(state_dir.is_relative_to(r) for r in roots):
        roots.append(state_dir)

    return roots


def _resolve_contained_path(
    path_str: str,
    allowed_roots: list[pathlib.Path],
) -> pathlib.Path | None:
    """Resolve *path_str* and verify it lies within one of *allowed_roots*.

    Returns the fully-resolved :class:`~pathlib.Path` when the path is
    safe, or ``None`` when it escapes the allowed roots (including via
    symlinks) or cannot be resolved.
    """
    try:
        resolved = pathlib.Path(path_str).resolve()
    except Exception:  # noqa: BLE001
        logger.debug("Failed to resolve path %r for containment check", path_str, exc_info=True)
        return None
    for root in allowed_roots:
        try:
            if resolved.is_relative_to(root):
                return resolved
        except Exception:  # noqa: BLE001
            logger.debug(
                "Failed to check containment of %r against root %r",
                path_str,
                root,
                exc_info=True,
            )
    return None


def register_all_builtins(registry: ConcreteToolRegistry) -> None:
    """Register all built-in tools into *registry*."""
    _register_git_tools(registry)
    _register_jira_tools(registry)
    _register_azure_devops_tools(registry)
    _register_github_tools(registry)
    _register_pull_request_thread_tool(registry)
    _register_filesystem_tools(registry)
    _register_testing_tools(registry)
    _register_state_tools(registry)


# ---------------------------------------------------------------------------
# Git tools
# ---------------------------------------------------------------------------


def _register_git_tools(registry: ConcreteToolRegistry) -> None:
    """Register Git domain tools."""
    from agentic_devtools.tools.git import (
        force_push,
        push,
        save_work,
        stage_changes,
    )

    registry.register(
        ToolDefinition(
            name="git_stage_all",
            description="Stage all changes (git add .)",
            category="git",
            input_schema={
                "type": "object",
                "properties": {"dry_run": {"type": "boolean"}},
            },
            mutating=True,
        ),
        fn=stage_changes,
    )

    registry.register(
        ToolDefinition(
            name="git_save_work",
            description="Stage, commit/amend, and push changes",
            category="git",
            input_schema={
                "type": "object",
                "properties": {
                    "commit_message": {"type": "string"},
                    "dry_run": {"type": "boolean"},
                },
                "required": ["commit_message"],
            },
            mutating=True,
        ),
        fn=save_work,
    )

    registry.register(
        ToolDefinition(
            name="git_push",
            description="Push to origin",
            category="git",
            input_schema={
                "type": "object",
                "properties": {"dry_run": {"type": "boolean"}},
            },
            mutating=True,
        ),
        fn=push,
    )

    registry.register(
        ToolDefinition(
            name="git_force_push",
            description="Force push to origin",
            category="git",
            input_schema={
                "type": "object",
                "properties": {"dry_run": {"type": "boolean"}},
            },
            mutating=True,
        ),
        fn=force_push,
    )

    def _git_get_current_branch() -> dict[str, Any]:
        """Get current branch name without sys.exit side effects."""
        from agentic_devtools.cli.git.core import run_git

        result = run_git("rev-parse", "--abbrev-ref", "HEAD", check=False)
        branch = result.stdout.strip() if result.stdout else ""
        if result.returncode != 0 or branch == "HEAD":
            return {"success": False, "branch": None, "message": "Detached HEAD or not a git repo"}
        return {"success": True, "branch": branch}

    registry.register(
        ToolDefinition(
            name="git_get_current_branch",
            description="Get the name of the current git branch",
            category="git",
            input_schema={"type": "object", "properties": {}},
            mutating=False,
        ),
        fn=_git_get_current_branch,
    )

    registry.register(
        ToolDefinition(
            name="git_current_branch",
            description="Get the name of the current git branch (alias)",
            category="git",
            input_schema={"type": "object", "properties": {}},
            mutating=False,
        ),
        fn=_git_get_current_branch,
    )

    def _git_get_status() -> dict[str, Any]:
        """Get git status (porcelain format)."""
        from agentic_devtools.cli.git.core import run_git

        result = run_git("status", "--porcelain", "--branch", check=False)
        if result.returncode != 0:
            return {"success": False, "output": "", "message": "Not a git repository"}
        return {"success": True, "output": result.stdout.strip()}

    registry.register(
        ToolDefinition(
            name="git_get_status",
            description="Get git status in porcelain format",
            category="git",
            input_schema={"type": "object", "properties": {}},
            mutating=False,
        ),
        fn=_git_get_status,
    )


# ---------------------------------------------------------------------------
# Jira tools
# ---------------------------------------------------------------------------


def _register_jira_tools(registry: ConcreteToolRegistry) -> None:
    """Register Jira domain tools."""
    from agentic_devtools.tools.jira import add_comment, fetch_issue_context

    def _jira_add_comment(issue_key: str, comment: str, **kwargs: Any) -> dict[str, Any]:
        """Add a comment to a Jira issue."""
        config = _get_jira_config()
        result = add_comment(config=config, issue_key=issue_key, comment=comment)
        return dict(result)

    registry.register(
        ToolDefinition(
            name="jira_add_comment",
            description="Add a comment to a Jira issue",
            category="jira",
            input_schema={
                "type": "object",
                "properties": {
                    "issue_key": {"type": "string", "description": "Jira issue key (e.g. PROJECT-123)"},
                    "comment": {"type": "string", "description": "Comment text"},
                },
                "required": ["issue_key", "comment"],
            },
            mutating=True,
        ),
        fn=_jira_add_comment,
    )

    def _jira_get_issue(issue_key: str, **kwargs: Any) -> dict[str, Any]:
        """Fetch Jira issue context."""
        config = _get_jira_config()
        result = fetch_issue_context(config=config, issue_key=issue_key)
        return dict(result)

    def _get_issue_context(
        issue_key: str | None = None,
        state: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch Jira issue context from explicit args or node state."""
        resolved_issue_key = _resolve_issue_context_issue_key(issue_key=issue_key, state=state)
        return _jira_get_issue(issue_key=resolved_issue_key)

    registry.register(
        ToolDefinition(
            name="jira_get_issue",
            description="Fetch Jira issue details and context",
            category="jira",
            input_schema={
                "type": "object",
                "properties": {
                    "issue_key": {"type": "string", "description": "Jira issue key"},
                },
                "required": ["issue_key"],
            },
            mutating=False,
        ),
        fn=_jira_get_issue,
    )

    # Backward-compatibility alias for poc_node.py
    registry.register(
        ToolDefinition(
            name="get_issue_context",
            description="Fetch Jira issue context (alias for jira_get_issue)",
            category="jira",
            input_schema={
                "type": "object",
                "properties": {
                    "issue_key": {"type": "string"},
                    "state": {
                        "type": "object",
                        "description": (
                            "Node state dict; issue_key resolved from state['issue_key'] when not provided directly"
                        ),
                    },
                },
            },
            mutating=False,
        ),
        fn=_get_issue_context,
    )


# ---------------------------------------------------------------------------
# Azure DevOps tools
# ---------------------------------------------------------------------------


def _register_azure_devops_tools(registry: ConcreteToolRegistry) -> None:
    """Register Azure DevOps domain tools."""
    from agentic_devtools.tools.azure_devops import (
        create_pull_request,
        reply_to_pull_request_thread,
        update_review_narrative,
    )

    def _ado_create_pr(
        source_branch: str,
        title: str,
        description: str = "",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a pull request in Azure DevOps."""
        from agentic_devtools.cli.azure_devops.auth import get_pat
        from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig

        config = AzureDevOpsConfig.from_state()
        pat = get_pat()
        result = create_pull_request(
            config=config,
            pat=pat,
            source_branch=source_branch,
            title=title,
            description=description,
        )
        return dict(result)

    registry.register(
        ToolDefinition(
            name="azure_devops_create_pr",
            description="Create a pull request in Azure DevOps",
            category="azure_devops",
            input_schema={
                "type": "object",
                "properties": {
                    "source_branch": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["source_branch", "title"],
            },
            mutating=True,
        ),
        fn=_ado_create_pr,
    )

    def _ado_reply_to_thread(
        pull_request_id: int,
        thread_id: int,
        content: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Reply to a PR thread."""
        from agentic_devtools.cli.azure_devops.auth import get_pat
        from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig

        config = AzureDevOpsConfig.from_state()
        pat = get_pat()
        result = reply_to_pull_request_thread(
            config=config,
            pat=pat,
            pull_request_id=pull_request_id,
            thread_id=thread_id,
            content=content,
        )
        return dict(result)

    registry.register(
        ToolDefinition(
            name="azure_devops_reply_to_thread",
            description="Reply to a pull request comment thread",
            category="azure_devops",
            input_schema={
                "type": "object",
                "properties": {
                    "pull_request_id": {"type": "integer"},
                    "thread_id": {"type": "integer"},
                    "content": {"type": "string"},
                },
                "required": ["pull_request_id", "thread_id", "content"],
            },
            mutating=True,
        ),
        fn=_ado_reply_to_thread,
    )

    def _ado_resolve_thread(pull_request_id: int, thread_id: int, **kwargs: Any) -> dict[str, Any]:
        """Resolve a PR thread."""
        from agentic_devtools.cli.azure_devops.auth import get_pat
        from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig

        config = AzureDevOpsConfig.from_state()
        pat = get_pat()
        result = reply_to_pull_request_thread(
            config=config,
            pat=pat,
            pull_request_id=pull_request_id,
            thread_id=thread_id,
            content="Resolved.",
            resolve_thread=True,
        )
        return dict(result)

    registry.register(
        ToolDefinition(
            name="azure_devops_resolve_thread",
            description="Resolve a pull request comment thread",
            category="azure_devops",
            input_schema={
                "type": "object",
                "properties": {
                    "pull_request_id": {"type": "integer"},
                    "thread_id": {"type": "integer"},
                },
                "required": ["pull_request_id", "thread_id"],
            },
            mutating=True,
        ),
        fn=_ado_resolve_thread,
    )

    def _ado_approve_pr(pull_request_id: int, content: str = "", **kwargs: Any) -> dict[str, Any]:
        """Approve a pull request."""
        from agentic_devtools.cli.azure_devops.auth import get_pat
        from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig

        config = AzureDevOpsConfig.from_state()
        pat = get_pat()
        result = update_review_narrative(
            config=config,
            pat=pat,
            pull_request_id=pull_request_id,
            content=content,
        )
        return dict(result)

    registry.register(
        ToolDefinition(
            name="azure_devops_approve_pull_request",
            description="Approve a pull request with review narrative update",
            category="azure_devops",
            input_schema={
                "type": "object",
                "properties": {
                    "pull_request_id": {"type": "integer"},
                    "content": {"type": "string"},
                },
                "required": ["pull_request_id"],
            },
            mutating=True,
        ),
        fn=_ado_approve_pr,
    )


# ---------------------------------------------------------------------------
# GitHub tools
# ---------------------------------------------------------------------------


def _register_pull_request_thread_tool(registry: ConcreteToolRegistry) -> None:
    """Register the provider-neutral PR discussion reply operation."""

    def _reply_to_thread(
        provider: str,
        repository: str,
        pull_request_number: int,
        discussion_id: int | str,
        body: str,
        resolve: bool = False,
        review_thread_id: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        from agentic_devtools.cli.pull_request_thread import reply_to_pull_request_thread

        try:
            result = reply_to_pull_request_thread(
                {
                    "provider": provider,
                    "repository": repository,
                    "pull_request_number": pull_request_number,
                    "discussion_id": discussion_id,
                    "body": body,
                    "resolve": resolve,
                    "review_thread_id": review_thread_id,
                }
            )
            result_dict = result.to_dict()
            if result.mutation_status == "failed":
                result_dict["success"] = False
            return result_dict
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    registry.register(
        ToolDefinition(
            name="reply_to_pull_request_thread",
            description="Reply to an existing Azure DevOps or GitHub pull-request discussion",
            category="code_hosting",
            input_schema={
                "type": "object",
                "properties": {
                    "provider": {"type": "string", "enum": ["azure_devops", "github"]},
                    "repository": {"type": "string"},
                    "pull_request_number": {"type": "integer"},
                    "discussion_id": {"oneOf": [{"type": "integer"}, {"type": "string"}]},
                    "body": {"type": "string"},
                    "resolve": {"type": "boolean"},
                    "review_thread_id": {"type": "string"},
                },
                "required": ["provider", "repository", "pull_request_number", "discussion_id", "body"],
            },
            mutating=True,
        ),
        fn=_reply_to_thread,
    )


def _register_github_tools(registry: ConcreteToolRegistry) -> None:
    """Register GitHub domain tools."""

    def _github_get_pr_state(pr_number: int, repo: str = "", **kwargs: Any) -> dict[str, Any]:
        """Get PR state from GitHub (side-effect-free, no state writes)."""
        from agentic_devtools.cli.github.pr_state import _evaluate_terminal_condition, _fetch_pr_with_retry

        data = _fetch_pr_with_retry(pr_number, repo)
        pr_state = data.get("state", "")
        head_ref_oid = data.get("headRefOid") or ""
        merged_at = data.get("mergedAt")
        locked = data.get("locked")
        is_terminal, terminal_reason = _evaluate_terminal_condition(pr_state, merged_at, locked)
        return {
            "prNumber": pr_number,
            "repo": repo,
            "state": pr_state,
            "headRefOid": head_ref_oid,
            "headRefOidShort": head_ref_oid[:7] if head_ref_oid else "",
            "mergeable": data.get("mergeable"),
            "mergeStateStatus": data.get("mergeStateStatus"),
            "isDraft": data.get("isDraft", False),
            "isTerminal": is_terminal,
            "terminalReason": terminal_reason,
        }

    registry.register(
        ToolDefinition(
            name="github_get_pr_state",
            description="Get the state of a GitHub pull request",
            category="github",
            input_schema={
                "type": "object",
                "properties": {
                    "pr_number": {"type": "integer", "description": "PR number"},
                    "repo": {"type": "string", "description": "owner/repo format"},
                },
                "required": ["pr_number"],
            },
            mutating=False,
        ),
        fn=_github_get_pr_state,
    )

    def _github_get_pr_checks(pr_number: int, repo: str = "", **kwargs: Any) -> dict[str, Any]:
        """Get PR checks status from GitHub (wraps _fetch_pr_checks safely)."""
        from agentic_devtools.cli.github.pr_checks_status import _fetch_pr_checks

        try:
            checks = _fetch_pr_checks(pr_number=pr_number, repo=repo)
            failed = [c for c in checks if c.get("conclusion") in ("failure", "cancelled")]
            pending = [c for c in checks if c.get("status") != "completed"]
            return {
                "success": True,
                "checks": checks,
                "total": len(checks),
                "failed_count": len(failed),
                "pending_count": len(pending),
            }
        except SystemExit:
            return {"success": False, "checks": [], "error": "gh CLI not available or failed"}

    registry.register(
        ToolDefinition(
            name="github_get_pr_checks_status",
            description="Get CI check status for a GitHub pull request",
            category="github",
            input_schema={
                "type": "object",
                "properties": {
                    "pr_number": {"type": "integer"},
                    "repo": {"type": "string"},
                },
                "required": ["pr_number"],
            },
            mutating=False,
        ),
        fn=_github_get_pr_checks,
    )

    def _github_add_comment(issue_number: str, comment: str, repo: str = "", **kwargs: Any) -> dict[str, Any]:
        """Add a comment to a GitHub issue."""
        from agentic_devtools.adapters.github_adapter import GitHubIssuesAdapter
        from agentic_devtools.cli.github.repo_resolution import resolve_github_repo_safe
        from agentic_devtools.orchestration.nodes._helpers import normalize_github_issue_number

        resolved_repo = repo or resolve_github_repo_safe() or ""
        if not resolved_repo:
            return {"success": False, "error": "Cannot resolve GitHub repo"}
        normalized = normalize_github_issue_number(issue_number)
        if not normalized:
            return {"success": False, "error": "issue_number must be a positive integer (e.g., '42' or '#42')"}
        try:
            adapter = GitHubIssuesAdapter(repo=resolved_repo)
            adapter.add_comment(normalized, comment)
            return {"success": True}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    registry.register(
        ToolDefinition(
            name="github_add_comment",
            description="Add a comment to a GitHub issue",
            category="github",
            input_schema={
                "type": "object",
                "properties": {
                    "issue_number": {
                        "type": "string",
                        "description": "GitHub issue number (e.g. '42' or '#42')",
                    },
                    "comment": {"type": "string", "description": "Comment text (Markdown)"},
                    "repo": {"type": "string", "description": "owner/repo (optional, auto-detected from git remote)"},
                },
                "required": ["issue_number", "comment"],
            },
            mutating=True,
        ),
        fn=_github_add_comment,
    )


# ---------------------------------------------------------------------------
# Filesystem tools
# ---------------------------------------------------------------------------


def _register_filesystem_tools(registry: ConcreteToolRegistry) -> None:
    """Register filesystem domain tools."""

    def _read_file(path: str, **kwargs: Any) -> dict[str, Any]:
        """Read a file and return its contents."""
        safe = _resolve_contained_path(path, _get_allowed_roots())
        if safe is None:
            return {
                "success": False,
                "content": None,
                "error": f"Path is outside allowed roots: {path}",
            }
        if not safe.exists():
            return {"success": False, "content": None, "error": f"File not found: {path}"}
        if not safe.is_file():
            return {"success": False, "content": None, "error": f"Not a file: {path}"}
        try:
            content = safe.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            return {
                "success": False,
                "content": None,
                "error": f"Failed to read file: {safe} ({type(exc).__name__}: {exc})",
            }
        return {"success": True, "content": content}

    registry.register(
        ToolDefinition(
            name="filesystem_read_file",
            description="Read a file and return its text content",
            category="filesystem",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute or relative file path"},
                },
                "required": ["path"],
            },
            mutating=False,
        ),
        fn=_read_file,
    )

    def _write_file(path: str, content: str, **kwargs: Any) -> dict[str, Any]:
        """Write content to a file."""
        safe = _resolve_contained_path(path, _get_allowed_roots())
        if safe is None:
            return {
                "success": False,
                "error": f"Path is outside allowed roots: {path}",
            }
        try:
            safe.parent.mkdir(parents=True, exist_ok=True)
            safe.write_text(content, encoding="utf-8")
        except OSError as exc:
            return {
                "success": False,
                "error": f"Failed to write file: {safe} ({type(exc).__name__}: {exc})",
            }
        return {"success": True, "path": str(safe), "bytes_written": len(content.encode("utf-8"))}

    registry.register(
        ToolDefinition(
            name="filesystem_write_file",
            description="Write text content to a file",
            category="filesystem",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to write"},
                    "content": {"type": "string", "description": "Content to write"},
                },
                "required": ["path", "content"],
            },
            mutating=True,
        ),
        fn=_write_file,
    )

    def _list_directory(path: str = ".", **kwargs: Any) -> dict[str, Any]:
        """List directory contents."""
        safe = _resolve_contained_path(path, _get_allowed_roots())
        if safe is None:
            return {
                "success": False,
                "entries": [],
                "error": f"Path is outside allowed roots: {path}",
            }
        if not safe.exists():
            return {"success": False, "entries": [], "error": f"Directory not found: {path}"}
        if not safe.is_dir():
            return {"success": False, "entries": [], "error": f"Not a directory: {path}"}
        try:
            entries = [{"name": e.name, "is_dir": e.is_dir()} for e in sorted(safe.iterdir())]
        except OSError as exc:
            return {
                "success": False,
                "entries": [],
                "error": f"Failed to list directory: {safe} ({type(exc).__name__}: {exc})",
            }
        return {"success": True, "entries": entries}

    registry.register(
        ToolDefinition(
            name="filesystem_list_directory",
            description="List the contents of a directory",
            category="filesystem",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path"},
                },
            },
            mutating=False,
        ),
        fn=_list_directory,
    )


# ---------------------------------------------------------------------------
# Testing tools
# ---------------------------------------------------------------------------


_STDOUT_TAIL_LIMIT = 2000
_STDERR_TAIL_LIMIT = 1000

# Pattern must be a valid pytest node id or path — reject shell metacharacters.
_SAFE_PATTERN_RE = re.compile(r"^[a-zA-Z0-9_\-./:\[\]@ ]+$")


def _validate_test_pattern(pattern: str) -> str | None:
    """Validate a pytest pattern string for safety.

    Returns an error message string when the pattern is unsafe, or ``None``
    when it is safe to pass directly to pytest.

    Rejects:
    - Patterns containing shell metacharacters (not matched by ``_SAFE_PATTERN_RE``)
    - Absolute paths (starting with ``/`` or a Windows drive letter such as ``C:``)
    - Path traversal segments (any ``..`` component)
    """
    if not _SAFE_PATTERN_RE.match(pattern):
        return "Invalid test pattern: contains disallowed characters"
    # Reject absolute paths (Unix: starts with /, Windows: drive-letter colon)
    if pattern.startswith("/"):
        return "Invalid test pattern: absolute paths are not allowed"
    if len(pattern) >= 2 and pattern[1] == ":" and pattern[0].isalpha():
        return "Invalid test pattern: absolute paths are not allowed"
    # Reject path traversal: split on both / and \ to catch all separators
    parts = re.split(r"[/\\]", pattern)
    if ".." in parts:
        return "Invalid test pattern: path traversal segments ('..') are not allowed"
    return None


def _register_testing_tools(registry: ConcreteToolRegistry) -> None:
    """Register testing domain tools."""

    def _run_tests(pattern: str = "", **kwargs: Any) -> dict[str, Any]:
        """Run pytest directly via subprocess with optional pattern filter."""
        if pattern:
            error_msg = _validate_test_pattern(pattern)
            if error_msg is not None:
                return {
                    "success": False,
                    "returncode": -1,
                    "stdout": "",
                    "stderr": error_msg,
                }
            return _run_pytest_subprocess(extra_args=[pattern])
        return _run_pytest_subprocess()

    registry.register(
        ToolDefinition(
            name="testing_run_tests",
            description="Run pytest with optional pattern filter",
            category="testing",
            input_schema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Test file or pattern to run"},
                },
            },
            mutating=False,
            timeout_seconds=120.0,
            thread_safe=False,
        ),
        fn=_run_tests,
    )

    def _run_test_pattern(pattern: str, **kwargs: Any) -> dict[str, Any]:
        """Run specific tests by pattern via direct pytest subprocess."""
        error_msg = _validate_test_pattern(pattern)
        if error_msg is not None:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": error_msg,
            }

        return _run_pytest_subprocess(extra_args=[pattern])

    registry.register(
        ToolDefinition(
            name="testing_run_pattern",
            description="Run specific tests matching a pattern",
            category="testing",
            input_schema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Test pattern (e.g. tests/test_foo.py::TestClass)"},
                },
                "required": ["pattern"],
            },
            mutating=False,
            timeout_seconds=120.0,
            thread_safe=False,
        ),
        fn=_run_test_pattern,
    )


# ---------------------------------------------------------------------------
# State tools
# ---------------------------------------------------------------------------


def _register_state_tools(registry: ConcreteToolRegistry) -> None:
    """Register state management domain tools."""
    from agentic_devtools.state import get_value, set_value

    def _state_get(key: str, **kwargs: Any) -> dict[str, Any]:
        """Get a value from state."""
        value = get_value(key)
        return {"key": key, "value": value, "found": value is not None}

    registry.register(
        ToolDefinition(
            name="state_get",
            description="Get a value from the agdt state store",
            category="state",
            input_schema={
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "State key to retrieve"},
                },
                "required": ["key"],
            },
            mutating=False,
            thread_safe=False,
        ),
        fn=_state_get,
    )

    def _state_set(key: str, value: Any = None, **kwargs: Any) -> dict[str, Any]:
        """Set a value in state."""
        set_value(key, value)
        return {"key": key, "value": value, "success": True}

    registry.register(
        ToolDefinition(
            name="state_set",
            description="Set a value in the agdt state store",
            category="state",
            input_schema={
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "State key to set"},
                    "value": {"description": "Value to store"},
                },
                "required": ["key"],
            },
            mutating=True,
            thread_safe=False,
        ),
        fn=_state_set,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_jira_config() -> Any:
    """Build JiraConfig from environment/state.

    This is a lazy helper that constructs the config at call time,
    allowing tests to mock the environment.
    """
    import os

    from agentic_devtools.cli.jira.config import get_jira_headers
    from agentic_devtools.tools.jira import JiraConfig

    base_url = os.environ.get("JIRA_BASE_URL", "https://jira.swica.ch")
    headers = get_jira_headers()

    ssl_verify: bool | str = True
    if os.environ.get("JIRA_SSL_VERIFY") == "0":
        ssl_verify = False
    elif os.environ.get("JIRA_CA_BUNDLE"):
        ssl_verify = os.environ["JIRA_CA_BUNDLE"]

    return JiraConfig(base_url=base_url, headers=headers, ssl_verify=ssl_verify)


def _normalize_issue_key(candidate: Any) -> str | None:
    """Normalize issue-key-like values to a non-empty string."""
    if type(candidate) is int:  # noqa: E721 - exclude bool
        return str(candidate)
    if isinstance(candidate, str):
        stripped = candidate.strip()
        if stripped:
            return stripped
    return None


def _resolve_issue_context_issue_key(
    *,
    issue_key: str | None,
    state: dict[str, Any] | None,
) -> str:
    """Resolve the issue key for the PoC-compatible get_issue_context alias."""
    if resolved := _normalize_issue_key(issue_key):
        return resolved

    if isinstance(state, dict):
        jira_state = state.get("jira")
        for candidate in (
            state.get("issue_key"),
            state.get("jira.issue_key"),
            state.get("jira_issue_key"),
            jira_state.get("issue_key") if isinstance(jira_state, dict) else None,
        ):
            if resolved := _normalize_issue_key(candidate):
                return resolved

        workflow = state.get("workflow")
        if isinstance(workflow, dict):
            context = workflow.get("context")
            if isinstance(context, dict) and (resolved := _normalize_issue_key(context.get("jira_issue_key"))):
                return resolved

    from agentic_devtools.cli.git.commands import _get_issue_key_from_state

    if resolved := _get_issue_key_from_state():
        return resolved

    raise TypeError("issue_key is required")


def _trim_testing_output(text: str, *, limit: int) -> str:
    """Trim captured test output to a bounded tail."""
    return text[-limit:] if len(text) > limit else text


def _run_pytest_subprocess(
    extra_args: list[str] | None = None,
) -> dict[str, Any]:
    """Run pytest directly via subprocess, capturing stdout and stderr.

    Avoids sys.argv mutation and redirect_stdout tricks that cannot capture
    output written by child processes directly to file-descriptor 1.
    Always uses ``shell=False`` to prevent shell-injection from caller-supplied
    pattern arguments.
    """
    from agentic_devtools.cli.testing import _try_get_workspace_root

    workspace_root = _try_get_workspace_root()
    if workspace_root is None:
        return {
            "success": False,
            "returncode": 1,
            "stdout": "",
            "stderr": "Could not resolve workspace root",
        }

    args: list[str] = [sys.executable, "-m", "pytest", "-v", "--tb=short"]
    if extra_args:
        args.append("--")
        args.extend(extra_args)

    proc = subprocess.run(
        args,
        capture_output=True,
        text=True,
        check=False,
        shell=False,
        cwd=str(workspace_root),
    )
    return {
        "success": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": _trim_testing_output(proc.stdout, limit=_STDOUT_TAIL_LIMIT),
        "stderr": _trim_testing_output(proc.stderr, limit=_STDERR_TAIL_LIMIT),
    }


def _capture_testing_sync(command: Any) -> dict[str, Any]:
    """Capture stdout/stderr for a synchronous AGDT test helper."""
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
        returncode = int(command())
    stdout = _trim_testing_output(stdout_buffer.getvalue(), limit=_STDOUT_TAIL_LIMIT)
    stderr = _trim_testing_output(stderr_buffer.getvalue(), limit=_STDERR_TAIL_LIMIT)
    return {
        "success": returncode == 0,
        "returncode": returncode,
        "stdout": stdout,
        "stderr": stderr,
    }


def _capture_testing_command(*, argv: list[str], command: Any) -> dict[str, Any]:
    """Capture stdout/stderr for an AGDT test command that exits via SystemExit."""
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    original_argv = sys.argv
    try:
        sys.argv = argv
        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
            try:
                command()
                returncode = 0
            except SystemExit as exc:
                if isinstance(exc.code, int):
                    returncode = exc.code
                elif exc.code is None:
                    returncode = 0
                else:
                    returncode = 1
    finally:
        sys.argv = original_argv
    stdout = _trim_testing_output(stdout_buffer.getvalue(), limit=_STDOUT_TAIL_LIMIT)
    stderr = _trim_testing_output(stderr_buffer.getvalue(), limit=_STDERR_TAIL_LIMIT)
    return {
        "success": returncode == 0,
        "returncode": returncode,
        "stdout": stdout,
        "stderr": stderr,
    }
