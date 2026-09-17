"""Provider-neutral command for marking pull requests as draft."""

from __future__ import annotations

import json
import os
import sys
from collections.abc import Callable
from typing import Any

from agentic_devtools.adapters.pull_request_draft import (
    AzureDevOpsPullRequestDraftAdapter,
    GitHubPullRequestDraftAdapter,
    PullRequestDraftRequest,
    PullRequestDraftResult,
)
from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.cli.azure_devops.commands import mark_pull_request_draft as _mark_azure_draft
from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.github.repo_resolution import resolve_github_repo_safe
from agentic_devtools.config import load_platform_config
from agentic_devtools.state import get_repo_root, get_value, is_dry_run
from agentic_devtools.task_state import print_task_tracking_info

_PROVIDERS = frozenset({"azure_devops", "github"})
_MODULE = "agentic_devtools.cli.pull_request_draft"
_StateLookup = Callable[[str], object | None]


def resolve_draft_provider(
    provider: str | None = None,
    state_lookup: _StateLookup | None = None,
) -> str:
    """Resolve the configured code-hosting provider."""
    lookup = state_lookup or get_value
    configured = provider if provider is not None else lookup("platform.code_hosting")
    if configured is None:
        root = get_repo_root()
        if root is not None:
            configured = load_platform_config(str(root)).get("code_hosting")
    if not isinstance(configured, str) or configured not in _PROVIDERS:
        raise ValueError("platform.code_hosting must be 'azure_devops' or 'github'")
    return configured


def _resolve_github_repo_from_config() -> str | None:
    """Resolve ``platform.github.repo`` from ``.github/agdt-config.json``, if present."""
    root = get_repo_root()
    if root is None:
        return None
    github_cfg = load_platform_config(str(root)).get("github")
    if not isinstance(github_cfg, dict):
        return None
    repo = github_cfg.get("repo")
    if repo is not None and not isinstance(repo, str):
        raise ValueError(
            f"platform.github.repo must be a string, got {type(repo).__name__!r}; fix .github/agdt-config.json"
        )
    return repo if isinstance(repo, str) and repo.strip() else None


def build_draft_request(
    *,
    provider: str | None = None,
    repository: str | None = None,
    pull_request_id: str | int | None = None,
    dry_run: bool | None = None,
) -> PullRequestDraftRequest:
    """Resolve state and validate a draft request."""
    selected = resolve_draft_provider(provider)
    raw_id: object = pull_request_id if pull_request_id is not None else get_value("pull_request_id")
    if raw_id is None and selected == "github":
        raw_id = get_value("github.pull_request_number")
    if not isinstance(raw_id, (str, int)) or isinstance(raw_id, bool):
        raise ValueError("pull_request_id must be a positive integer")
    try:
        pr_id = int(raw_id)
    except (TypeError, ValueError) as exc:
        raise ValueError("pull_request_id must be a positive integer") from exc
    organization: str | None = None
    project: str | None = None
    if repository is not None and not isinstance(repository, str):
        raise ValueError(
            f"repository must be a string, got {type(repository).__name__!r}; "
            "use agdt-set to store an owner/repo string"
        )
    if selected == "github":
        state_repo = get_value("github.repo")
        if state_repo is not None and not isinstance(state_repo, str):
            raise ValueError(
                f"github.repo must be a string, got {type(state_repo).__name__!r}; "
                "use agdt-set to store an owner/repo string"
            )
        env_repo = os.environ.get("GITHUB_REPOSITORY")
        repo = (
            (repository if isinstance(repository, str) and repository.strip() else None)
            or (state_repo if isinstance(state_repo, str) and state_repo.strip() else None)
            or (env_repo if isinstance(env_repo, str) and env_repo.strip() else None)
            or _resolve_github_repo_from_config()
            or resolve_github_repo_safe()
        )
    else:
        ado_config = AzureDevOpsConfig.from_state()
        repo = repository or ado_config.repository
        organization = ado_config.organization
        project = ado_config.project
    if not isinstance(repo, str) or not repo.strip():
        raise ValueError("repository is required")
    return PullRequestDraftRequest(
        selected,
        repo.strip(),
        pr_id,
        is_dry_run() if dry_run is None else dry_run,
        organization=organization,
        project=project,
    )


def dispatch_draft(request: PullRequestDraftRequest) -> PullRequestDraftResult:
    """Dispatch a validated request to its provider adapter."""
    if request.provider == "github":
        return GitHubPullRequestDraftAdapter().mark_draft(request)
    return AzureDevOpsPullRequestDraftAdapter(
        lambda req: _mark_azure_draft(
            pull_request_id=req.pull_request_id,
            exit_on_error=False,
            organization=req.organization,
            project=req.project,
            dry_run=req.dry_run,
        )
    ).mark_draft(request)


def mark_pull_request_draft(**kwargs: Any) -> PullRequestDraftResult:
    """Mark a pull request as draft and print its structured result."""
    try:
        result = dispatch_draft(build_draft_request(**kwargs))
    except Exception as exc:
        result = PullRequestDraftResult(False, str(kwargs.get("provider") or "unknown"), "invalid", str(exc)[:1000])
    print(json.dumps(result.__dict__, ensure_ascii=False))
    return result


def _run_request_snapshot(**kwargs: Any) -> int:
    """Dispatch an immutable request snapshot and return a task exit status."""
    request = PullRequestDraftRequest(**kwargs)
    result = dispatch_draft(request)
    print(json.dumps(result.__dict__, ensure_ascii=False))
    return 0 if result.success else 1


def mark_pull_request_draft_async(
    provider: str | None = None,
    repository: str | None = None,
    pull_request_id: str | int | None = None,
) -> None:
    """Snapshot request fields and run the provider-neutral command in a task."""
    try:
        request = build_draft_request(
            provider=provider,
            repository=repository,
            pull_request_id=pull_request_id,
        )
    except Exception as exc:
        result = PullRequestDraftResult(
            False,
            str(provider or "unknown"),
            "invalid",
            str(exc)[:1000],
        )
        print(json.dumps(result.__dict__, ensure_ascii=False))
        sys.exit(1)
    task = run_function_in_background(
        _MODULE,
        "_run_request_snapshot",
        command_display_name="agdt-mark-pull-request-draft",
        func_kwargs=request.__dict__,
    )
    print_task_tracking_info(task, "Marking pull request as draft")
