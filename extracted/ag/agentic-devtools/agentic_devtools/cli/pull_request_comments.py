"""Provider-neutral pull-request comment command."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections.abc import Callable
from typing import Any

from agentic_devtools.adapters.pull_request_comments import (
    AzureDevOpsPullRequestCommentAdapter,
    GitHubPullRequestCommentAdapter,
    PullRequestCommentAdapter,
    PullRequestCommentRequest,
    PullRequestCommentResult,
)
from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.cli.azure_devops.auth import get_pat
from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.helpers import parse_bool_from_state_value
from agentic_devtools.cli.github.repo_resolution import resolve_github_repo_safe
from agentic_devtools.config import load_platform_config
from agentic_devtools.state import get_repo_root, get_value, is_dry_run
from agentic_devtools.task_state import print_task_tracking_info

_MODULE = "agentic_devtools.cli.pull_request_comments"
_PROVIDERS = frozenset({"azure_devops", "github"})
_StateLookup = Callable[[str], object | None]
_DEFAULT_STATE_LOOKUP = object()


def _normalize_state_lookup(state_lookup: _StateLookup | None | object) -> _StateLookup | None:
    """Resolve the default sentinel to the current module-level state getter."""
    if state_lookup is _DEFAULT_STATE_LOOKUP:
        return get_value
    return state_lookup if callable(state_lookup) else None


def _state_or(value: object, *keys: str) -> object:
    """Return an explicit value, otherwise the first matching state value."""
    if value is not None:
        return value
    for key in keys:
        found = get_value(key)
        if found is not None:
            return found
    return None


def _as_int(value: object, name: str) -> int | None:
    """Convert an optional state/CLI number and reject malformed values."""
    if value is None or value == "":
        return None
    try:
        if not isinstance(value, (str, int)) or isinstance(value, bool):
            raise TypeError
        converted = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a positive integer") from exc
    if converted <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return converted


def resolve_comment_provider(
    provider: str | None = None,
    state_lookup: _StateLookup | None | object = _DEFAULT_STATE_LOOKUP,
) -> str:
    """Resolve an explicitly configured code-hosting provider.

    Credentials are never used to select a provider.
    """
    resolved_state_lookup = _normalize_state_lookup(state_lookup)
    configured = (
        provider
        if provider is not None
        else resolved_state_lookup("platform.code_hosting")
        if resolved_state_lookup
        else None
    )
    if configured is None:
        root = get_repo_root()
        if root is not None:
            configured = load_platform_config(str(root)).get("code_hosting")
    if not isinstance(configured, str) or configured not in _PROVIDERS:
        raise ValueError("platform.code_hosting must be 'azure_devops' or 'github'")
    return configured


def _resolve_repository(
    provider: str,
    repository: str | None,
    state_lookup: _StateLookup | None | object = _DEFAULT_STATE_LOOKUP,
) -> str:
    """Resolve and validate the repository without consulting credentials."""
    resolved_state_lookup = _normalize_state_lookup(state_lookup)
    if provider == "github":
        explicit = (
            repository
            if repository is not None
            else resolved_state_lookup("github.repo")
            if resolved_state_lookup
            else None
        )
    else:
        explicit = (
            repository
            if repository is not None
            else resolved_state_lookup("repository")
            if resolved_state_lookup
            else None
        )
    if explicit is not None and not isinstance(explicit, str):
        raise ValueError(
            f"repository must be a string, got {type(explicit).__name__!r}; use agdt-set to store an owner/repo string"
        )
    if isinstance(explicit, str) and explicit.strip():
        resolved = explicit.strip()
    elif provider == "github":
        resolved = os.environ.get("GITHUB_REPOSITORY", "").strip() or (resolve_github_repo_safe() or "")
    else:
        resolved = AzureDevOpsConfig.from_state().repository.strip() if resolved_state_lookup else ""
    if not resolved:
        raise ValueError("repository is required")
    if provider == "github" and (
        resolved.count("/") != 1
        or any(not part.strip() or any(char.isspace() for char in part) for part in resolved.split("/"))
    ):
        raise ValueError("GitHub repository must be in owner/repo form")
    return resolved


def _build_request(
    *,
    provider: str | None = None,
    repository: str | None = None,
    pull_request_id: str | int | None = None,
    content: str | None = None,
    path: str | None = None,
    line: str | int | None = None,
    end_line: str | int | None = None,
    resolve_after_posting: bool | None = None,
    dry_run: bool | None = None,
    idempotency_marker: str | None = None,
    use_state_defaults: bool = True,
) -> PullRequestCommentRequest:
    """Resolve state and validate one immutable request snapshot."""
    state_lookup = get_value if use_state_defaults else None
    selected = resolve_comment_provider(provider, state_lookup=state_lookup)
    state_or = _state_or if use_state_defaults else lambda value, *_keys: value
    pr_id = _as_int(
        state_or(pull_request_id, "pull_request_id", "github.pull_request_number", "pr_number"), "pull_request_id"
    )
    if pr_id is None:
        raise ValueError("pull_request_id is required")
    body = state_or(content, "content", "comment")
    if not isinstance(body, str) or not body.strip():
        raise ValueError("content is required")
    resolved_repository = _resolve_repository(selected, repository, state_lookup=state_lookup)
    marker = state_or(idempotency_marker, "idempotency_marker", "comment_marker")
    if marker is not None and not isinstance(marker, str):
        raise ValueError("idempotency_marker must be a string")
    if marker is None:
        digest = hashlib.sha256(f"{selected}\0{resolved_repository}\0{pr_id}\0{body}".encode()).hexdigest()
        marker = f"<!-- agdt-comment-{digest} -->"
    leave_active = get_value("leave_thread_active") if use_state_defaults else None
    resolve = (
        resolve_after_posting
        if resolve_after_posting is not None
        else not parse_bool_from_state_value(leave_active, default=False)
    )
    raw_path = state_or(path, "path")
    if raw_path is not None and not isinstance(raw_path, str):
        raise ValueError("path must be a string")
    ado_organization: str | None = None
    ado_project: str | None = None
    if selected == "azure_devops":
        ado_cfg = AzureDevOpsConfig.from_state()
        ado_organization = ado_cfg.organization
        ado_project = ado_cfg.project
    return PullRequestCommentRequest(
        provider=selected,
        repository=resolved_repository,
        pull_request_id=pr_id,
        content=body,
        path=raw_path or None,
        line=_as_int(state_or(line, "line"), "line"),
        end_line=_as_int(state_or(end_line, "end_line"), "end_line"),
        resolve_after_posting=resolve,
        dry_run=is_dry_run() if dry_run is None else dry_run,
        idempotency_marker=marker,
        organization=ado_organization,
        project=ado_project,
    )


def _adapter_for(request: PullRequestCommentRequest) -> PullRequestCommentAdapter:
    """Build the adapter selected by the request provider."""
    if request.provider == "github":
        return GitHubPullRequestCommentAdapter()
    if request.organization is None or request.project is None:
        config = AzureDevOpsConfig.from_state()
        organization = request.organization if request.organization is not None else config.organization
        project = request.project if request.project is not None else config.project
    else:
        organization = request.organization
        project = request.project
    return AzureDevOpsPullRequestCommentAdapter(
        AzureDevOpsConfig(organization, project, request.repository),
        "" if request.dry_run else get_pat(),
    )


def dispatch_pull_request_comment(request: PullRequestCommentRequest) -> PullRequestCommentResult:
    """Run readiness checks and dispatch one validated request."""
    try:
        adapter = _adapter_for(request)
        return adapter.add_comment(request)
    except Exception as exc:
        return PullRequestCommentResult(False, request.provider, "failed", error=str(exc)[:1000])


def add_pull_request_comment(**kwargs: Any) -> PullRequestCommentResult:
    """Add a provider-neutral pull-request comment from state or snapshots."""
    try:
        request = _build_request(**kwargs)
    except Exception as exc:
        result = PullRequestCommentResult(False, str(kwargs.get("provider") or "unknown"), "invalid", error=str(exc))
    else:
        result = dispatch_pull_request_comment(request)
    print(json.dumps(result.as_dict(), ensure_ascii=False))
    return result


def _run_request_snapshot(**kwargs: Any) -> int:
    """Dispatch an immutable request snapshot and return a task exit status."""
    request = PullRequestCommentRequest(**kwargs)
    result = dispatch_pull_request_comment(request)
    print(json.dumps(result.as_dict(), ensure_ascii=False))
    return 0 if result.success else 1


def add_pull_request_comment_async(
    pull_request_id: str | None = None,
    content: str | None = None,
    provider: str | None = None,
    repository: str | None = None,
) -> None:
    """Snapshot request fields and run the provider-neutral command in a task."""
    if (
        pull_request_id is None
        and content is None
        and provider is None
        and repository is None
        and len(sys.argv) > 1
        and any(argument.startswith("-") for argument in sys.argv[1:])
    ):
        parser = argparse.ArgumentParser(description="Add a comment to a pull request")
        parser.add_argument("-p", "--pull-request-id")
        parser.add_argument("-c", "--content")
        parser.add_argument("--provider")
        parser.add_argument("--repo")
        args = parser.parse_args()
        pull_request_id, content, provider, repository = args.pull_request_id, args.content, args.provider, args.repo

    try:
        request = _build_request(
            provider=provider,
            repository=repository,
            pull_request_id=pull_request_id,
            content=content,
        )
    except Exception as exc:
        result = PullRequestCommentResult(
            False,
            provider or "unknown",
            "invalid",
            error=str(exc)[:1000],
        )
        print(json.dumps(result.as_dict(), ensure_ascii=False))
        sys.exit(1)
    task = run_function_in_background(
        _MODULE,
        "_run_request_snapshot",
        command_display_name="agdt-add-pull-request-comment",
        func_kwargs=request.__dict__,
    )
    print_task_tracking_info(task, "Adding comment to pull request")
