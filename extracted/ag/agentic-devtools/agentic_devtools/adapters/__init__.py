"""Pluggable issue adapter package.

Public API
----------
- :class:`IssueAdapter` — abstract base class
- :class:`JiraAdapter`, :class:`GitHubIssuesAdapter`, :class:`MarkdownAdapter` — concrete adapters
- :func:`get_adapter` — factory that returns the correct adapter based on platform config
- Shared TypedDicts: :class:`IssueResult`, :class:`IssueDetail`, :class:`CommentResult`,
  :class:`IssueSummary`, :class:`IssueFilters`, :class:`Comment`,
  :class:`IssueTypeInfo`, :class:`PropertySchema`
- Pull-request thread reply contracts: :class:`PullRequestThreadReplyRequest`,
  :class:`PullRequestThreadReplyResult` (and their ``ReplyToPullRequestThread*`` aliases)
"""

from __future__ import annotations

import base64
import os
from pathlib import Path

from agentic_devtools.adapters.base import (
    Comment,
    CommentResult,
    IssueAdapter,
    IssueDetail,
    IssueDetailWithRaw,
    IssueFilters,
    IssueResult,
    IssueSummary,
    IssueTypeInfo,
    NormalizedIssue,
    PropertySchema,
    PullRequestThreadReplyRequest,
    PullRequestThreadReplyResult,
    ReplyToPullRequestThreadRequest,
    ReplyToPullRequestThreadResult,
)
from agentic_devtools.adapters.exceptions import (
    AdapterError,
    AdapterValidationError,
    HierarchyLinkError,
)
from agentic_devtools.adapters.factory import get_issue_provider, resolve_provider_name
from agentic_devtools.adapters.github_adapter import GitHubIssuesAdapter
from agentic_devtools.adapters.idempotency_query_provider import IdempotencyQueryProvider
from agentic_devtools.adapters.issue_provider import (
    VALID_ISSUE_TYPES,
    HierarchyValidationProvider,
    InMemoryIssueProvider,
    IssueProvider,
    IssueTypeMappingError,
    ProviderIssueResult,
    ProviderLinkResult,
)
from agentic_devtools.adapters.issue_type_mapping import (
    GitHubMappingResult,
    JiraMappingResult,
    TypeMapping,
    load_github_type_mapping,
    load_jira_type_mapping,
    map_issue_type_to_github_labels,
    map_issue_type_to_jira,
)
from agentic_devtools.adapters.jira_adapter import JiraAdapter
from agentic_devtools.adapters.markdown_adapter import MarkdownAdapter
from agentic_devtools.adapters.operation_plan import OperationDescriptor, OperationPlan
from agentic_devtools.adapters.orchestration_key import generate_orchestration_key
from agentic_devtools.adapters.plan_manifest import execute_manifest, plan_manifest
from agentic_devtools.adapters.pull_request_comments import (
    AzureDevOpsPullRequestCommentAdapter,
    GitHubPullRequestCommentAdapter,
    PullRequestCommentAdapter,
    PullRequestCommentCapability,
    PullRequestCommentRequest,
    PullRequestCommentResult,
    discover_github_token,
)
from agentic_devtools.adapters.pull_request_threads import (
    AzureDevOpsThreadResolutionAdapter,
    GitHubThreadResolutionAdapter,
    ThreadResolutionAdapter,
    ThreadResolutionCapability,
    ThreadResolutionRequest,
    ThreadResolutionResult,
)
from agentic_devtools.cli.config.project_config import load_effective_project_config
from agentic_devtools.config import load_platform_config
from agentic_devtools.tools.jira import JiraConfig

__all__ = [
    "AdapterError",
    "AdapterValidationError",
    "AzureDevOpsPullRequestCommentAdapter",
    "AzureDevOpsThreadResolutionAdapter",
    "Comment",
    "CommentResult",
    "GitHubIssuesAdapter",
    "GitHubMappingResult",
    "GitHubPullRequestCommentAdapter",
    "GitHubThreadResolutionAdapter",
    "HierarchyLinkError",
    "HierarchyValidationProvider",
    "IdempotencyQueryProvider",
    "InMemoryIssueProvider",
    "IssueAdapter",
    "IssueDetail",
    "IssueDetailWithRaw",
    "IssueFilters",
    "IssueProvider",
    "IssueResult",
    "IssueSummary",
    "IssueTypeMappingError",
    "IssueTypeInfo",
    "JiraAdapter",
    "JiraMappingResult",
    "MarkdownAdapter",
    "NormalizedIssue",
    "OperationDescriptor",
    "OperationPlan",
    "PropertySchema",
    "ProviderIssueResult",
    "ProviderLinkResult",
    "PullRequestCommentAdapter",
    "PullRequestCommentCapability",
    "PullRequestCommentRequest",
    "PullRequestCommentResult",
    "PullRequestThreadReplyRequest",
    "PullRequestThreadReplyResult",
    "ReplyToPullRequestThreadRequest",
    "ReplyToPullRequestThreadResult",
    "ThreadResolutionAdapter",
    "ThreadResolutionCapability",
    "ThreadResolutionRequest",
    "ThreadResolutionResult",
    "TypeMapping",
    "VALID_ISSUE_TYPES",
    "discover_github_token",
    "execute_manifest",
    "generate_orchestration_key",
    "get_adapter",
    "get_issue_provider",
    "load_github_type_mapping",
    "load_jira_type_mapping",
    "map_issue_type_to_github_labels",
    "map_issue_type_to_jira",
    "plan_manifest",
    "resolve_jira_config",
    "resolve_provider_name",
]


def get_adapter(repo_path: str) -> IssueAdapter:
    """Return an :class:`IssueAdapter` based on the platform configuration.

    Reads ``load_platform_config(repo_path)["issue_adapter"]`` and returns
    the matching adapter instance.  Adapter construction is eager but
    connectivity is validated lazily (adapter methods raise on failure).

    Args:
        repo_path: Absolute (or relative) path to the target repository root.

    Returns:
        A concrete :class:`IssueAdapter` instance.

    Raises:
        ValueError: If the configured adapter name is not recognised.
    """
    platform_config = load_platform_config(repo_path)
    adapter_name = platform_config["issue_adapter"]

    if adapter_name == "jira":
        return _build_jira_adapter(platform_config, git_root=repo_path)

    if adapter_name == "github":
        return _build_github_adapter(platform_config)

    if adapter_name == "markdown":
        markdown_config = platform_config.get("markdown")
        schema_override = markdown_config.get("schema_override") if isinstance(markdown_config, dict) else None
        return MarkdownAdapter(repo_path=repo_path, schema_override=schema_override)

    raise ValueError(f"Unknown issue adapter: {adapter_name}")


# ------------------------------------------------------------------
# Private builder helpers
# ------------------------------------------------------------------


def _resolve_jira_base_url(git_root: str | Path | None = None) -> str:
    """Resolve Jira base URL with optional repo-scoped fallback for setup probes."""
    project_config = load_effective_project_config(git_root=Path(git_root) if git_root is not None else None)
    project_base_url = project_config.get("jira_base_url")
    if isinstance(project_base_url, str) and project_base_url.strip():
        return project_base_url.strip()

    # Deferred import to avoid circular dependency during module initialization.
    from agentic_devtools.state import get_value

    state_base_url = get_value("jira_base_url")
    if isinstance(state_base_url, str) and state_base_url.strip():
        return state_base_url.strip()

    base_url = os.environ.get("JIRA_BASE_URL", "")
    return base_url.strip()


def resolve_jira_config(git_root: str | Path | None = None) -> JiraConfig:
    """Resolve the Jira connection settings shared by adapters and setup probes."""
    base_url = _resolve_jira_base_url(git_root)
    token = os.environ.get("JIRA_API_TOKEN", "") or os.environ.get("JIRA_COPILOT_PAT", "")
    identity = (
        os.environ.get("JIRA_USER_EMAIL", "") or os.environ.get("JIRA_EMAIL", "") or os.environ.get("JIRA_USERNAME", "")
    )
    auth_scheme = os.environ.get("JIRA_AUTH_SCHEME", "bearer").lower()

    headers: dict[str, str] = {"Content-Type": "application/json"}
    if identity or auth_scheme == "basic":
        if identity and token:
            credentials = base64.b64encode(f"{identity}:{token}".encode()).decode()
            headers["Authorization"] = f"Basic {credentials}"
    elif token:
        headers["Authorization"] = "Bearer " + token

    ssl_env = os.environ.get("JIRA_SSL_VERIFY", "").strip()
    ssl_verify: bool | str
    if ssl_env.lower() in ("0", "false"):
        ssl_verify = False
    elif ssl_env:
        ssl_verify = ssl_env
    else:
        from agentic_devtools.cli.jira.helpers import _get_repo_jira_pem_path
        from agentic_devtools.state import get_value

        state_ca_bundle = get_value("jira.ca_bundle_path")
        state_ca_bundle_path = state_ca_bundle.strip() if isinstance(state_ca_bundle, str) else ""
        if state_ca_bundle_path and Path(state_ca_bundle_path).exists():
            ssl_verify = state_ca_bundle_path
        else:
            ca_bundle = (os.environ.get("JIRA_CA_BUNDLE", "") or os.environ.get("REQUESTS_CA_BUNDLE", "")).strip()
            if ca_bundle:
                ssl_verify = ca_bundle
            else:
                repo_pem = (
                    Path(git_root) / "scripts" / "jira_ca_bundle.pem"
                    if git_root is not None
                    else _get_repo_jira_pem_path()
                )
                ssl_verify = str(repo_pem) if repo_pem.exists() else True

    return JiraConfig(base_url=base_url, headers=headers, ssl_verify=ssl_verify)


def _build_jira_adapter(platform_config: dict, git_root: str | Path | None = None) -> JiraAdapter:
    """Construct a :class:`JiraAdapter` from environment variables and config.

    Authentication follows the same conventions as
    :func:`agentic_devtools.mcp.server._load_jira_config`:

    * **Token** — ``JIRA_API_TOKEN`` falling back to ``JIRA_COPILOT_PAT``.
    * **Identity** — ``JIRA_USER_EMAIL`` → ``JIRA_EMAIL`` → ``JIRA_USERNAME``.
    * **Scheme** — ``JIRA_AUTH_SCHEME`` (default ``"bearer"``).  When the
      scheme is ``"basic"`` **or** an identity env var is set, Basic auth is
      attempted: the ``Authorization`` header is only added when **both**
      identity and token are present; otherwise no auth header is sent and
      the request will fail lazily at call time.  In all other cases, when a
      token is available, Bearer auth is used.

    SSL verification honours ``JIRA_SSL_VERIFY``, then falls back to
    state/env/repo certificate sources:

    * ``JIRA_SSL_VERIFY="0"`` or ``"false"`` → disabled (``False``).
    * ``JIRA_SSL_VERIFY`` set to any other non-empty value → CA bundle path.
    * ``jira.ca_bundle_path`` state key set → CA bundle path.
    * ``JIRA_CA_BUNDLE`` or ``REQUESTS_CA_BUNDLE`` set → CA bundle path.
    * Repo ``jira_ca_bundle.pem`` present → use that path.
    * Nothing set → strict verification (``True``).
    """
    config = resolve_jira_config(git_root)
    project_key = platform_config.get("jira", {}).get("project_key", "") or None
    return JiraAdapter(config=config, project_key=project_key)


def _build_github_adapter(platform_config: dict) -> GitHubIssuesAdapter:
    """Construct a :class:`GitHubIssuesAdapter` from platform config.

    Resolves the repository slug using the ``repo`` key first (canonical
    format written by auto-detection).  Falls back to concatenating
    ``repo_owner`` / ``repo_name`` for legacy configs.  All values are
    stripped; ``None`` entries are coerced to ``""`` so no exception is
    raised for any combination of present/absent keys.
    """
    _gh = platform_config.get("github")
    gh: dict[str, object] = _gh if isinstance(_gh, dict) else {}

    def _clean(value: object) -> str:
        return value.strip() if isinstance(value, str) else ""

    repo_slug = _clean(gh.get("repo"))
    if not repo_slug:
        repo_owner = _clean(gh.get("repo_owner"))
        repo_name = _clean(gh.get("repo_name"))
        repo_slug = f"{repo_owner}/{repo_name}" if repo_owner and repo_name else ""
    return GitHubIssuesAdapter(repo=repo_slug)
