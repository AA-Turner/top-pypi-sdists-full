"""Provider-neutral pull-request approval command."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from agentic_devtools.adapters.pull_request_approval import (
    AzureDevOpsPullRequestApprovalAdapter,
    GitHubPullRequestApprovalAdapter,
    PullRequestApprovalAdapter,
    PullRequestApprovalRequest,
    PullRequestApprovalResult,
    _sanitize_diagnostic,
)
from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.cli.azure_devops.commands import approve_pull_request as approve_azure_pull_request
from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.github.repo_resolution import resolve_github_repo_safe
from agentic_devtools.config import load_platform_config
from agentic_devtools.file_locking import locked_file
from agentic_devtools.state import get_repo_root, get_value, load_state_locked
from agentic_devtools.task_state import print_task_tracking_info

_MODULE = "agentic_devtools.cli.pull_request_approval"
_PROVIDERS = frozenset({"azure_devops", "github"})
_APPROVAL_LOCK_TIMEOUT_SECONDS = 300


def _approval_lock_path(request: PullRequestApprovalRequest) -> Path:
    """Return a stable lock path for the immutable provider approval target."""
    repository = (
        request.repository.removesuffix(".git").casefold()
        if request.provider == "github"
        else unquote(request.repository).casefold()
    )
    target = "\0".join(
        (
            request.provider,
            unquote(request.organization or "").rstrip("/").casefold() if request.provider == "azure_devops" else "",
            unquote(request.project or "").casefold() if request.provider == "azure_devops" else "",
            repository,
            str(request.pull_request_id),
        )
    )
    target_hash = hashlib.sha256(target.encode("utf-8")).hexdigest()
    return Path.home() / ".agdt" / "locks" / "pull-request-approval" / f"{target_hash}.lock"


def _state_value(state: Mapping[str, Any], key: str) -> Any:
    """Return a state value by dotted key from one loaded state mapping."""
    if key in state:
        return state[key]
    current: Any = state
    for part in key.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return None
        current = current[part]
    return current


def resolve_approval_provider(provider: str | None = None, state: Mapping[str, Any] | None = None) -> str:
    """Resolve provider from explicit input, state, or repository config."""
    configured = provider
    if configured is None:
        configured = (
            _state_value(state, "platform.code_hosting") if state is not None else get_value("platform.code_hosting")
        )
    legacy_unset = provider is None and configured == "other"
    if legacy_unset:
        configured = None
    if configured is None:
        root = get_repo_root()
        if root is not None:
            configured = load_platform_config(str(root)).get("code_hosting")
    if provider is None and configured == "other":
        configured = "azure_devops"
    if legacy_unset and configured is None:
        configured = "azure_devops"
    if not isinstance(configured, str) or configured not in _PROVIDERS:
        raise ValueError("platform.code_hosting must be 'azure_devops' or 'github'")
    return configured


def _state_or(value: object, *keys: str, state: Mapping[str, Any] | None = None) -> object:
    if value is not None:
        return value
    for key in keys:
        found = _state_value(state, key) if state is not None else get_value(key)
        if found is not None:
            return found
    return None


def _positive_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (str, int)) or value == "":
        raise ValueError(f"{name} must be a positive integer")
    try:
        number = int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a positive integer") from exc
    if number <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return number


def _resolve_approval_repository(
    provider: str,
    repository: str | None,
    *,
    azure_config: AzureDevOpsConfig | None = None,
    state: Mapping[str, Any] | None = None,
) -> str:
    explicit: object | None
    if repository is not None:
        explicit = repository
    elif provider == "github":
        explicit = _state_value(state, "github.repo") if state is not None else get_value("github.repo")
    else:
        explicit = (
            azure_config.repository
            if azure_config is not None
            else _state_value(state, "repository")
            if state is not None
            else get_value("repository")
        )
    if explicit is not None:
        if not isinstance(explicit, str) or not explicit.strip():
            raise ValueError("repository is required")
        resolved = explicit.strip()
    elif provider == "github":
        resolved = (resolve_github_repo_safe(state) if state is not None else resolve_github_repo_safe()) or ""
    else:
        config = (
            azure_config
            if azure_config is not None
            else AzureDevOpsConfig.from_state(state)
            if state is not None
            else AzureDevOpsConfig.from_state()
        )
        resolved = config.repository.strip()
    if not resolved:
        raise ValueError("repository is required")
    return resolved


def _build_approval_request(
    *,
    provider: str | None = None,
    repository: str | None = None,
    pull_request_id: str | int | None = None,
    content: str | None = None,
    expected_head: str | None = None,
    dry_run: bool | None = None,
) -> PullRequestApprovalRequest:
    """Build an immutable approval request from arguments and state."""
    state = load_state_locked()
    selected = resolve_approval_provider(provider, state)
    azure_config = AzureDevOpsConfig.from_state(state) if selected == "azure_devops" else None
    if selected == "github" and pull_request_id is None:
        stored_id = _state_value(state, "pull_request_id")
        github_id = _state_value(state, "github.pull_request_number")
        if stored_id is not None and github_id is not None:
            if _positive_int(stored_id, "pull_request_id") != _positive_int(github_id, "github.pull_request_number"):
                raise ValueError("Conflicting pull-request IDs in state; pass --pull-request-id explicitly")
    pr_id = (
        _state_or(pull_request_id, "pull_request_id", "github.pull_request_number", state=state)
        if selected == "github"
        else _state_or(pull_request_id, "pull_request_id", state=state)
    )
    body = _state_or(content, "content", state=state)
    head = (
        _state_or(
            expected_head,
            "sourceCodeHostingPlatform.pullRequest.headSha",
            "github.head_sha",
            "github.head_ref_oid",
            state=state,
        )
        if selected == "github"
        else expected_head
    )
    if dry_run is None:
        state_dry_run = _state_value(state, "dry_run")
        dry_run = (
            state_dry_run if isinstance(state_dry_run, bool) else str(state_dry_run).lower() in ("1", "true", "yes")
        )
    if not isinstance(body, str) or not body.strip():
        raise ValueError("content is required")
    if selected == "github" and head is not None and not isinstance(head, str):
        raise ValueError("expected_head must be a full 40-character lowercase hexadecimal SHA")
    return PullRequestApprovalRequest(
        provider=selected,  # type: ignore[arg-type]
        repository=_resolve_approval_repository(selected, repository, azure_config=azure_config, state=state),
        pull_request_id=_positive_int(pr_id, "pull_request_id"),
        content=body,
        expected_head=head if isinstance(head, str) else None,
        dry_run=dry_run,
        organization=azure_config.organization if azure_config is not None else None,
        project=azure_config.project if azure_config is not None else None,
    )


def _approve_azure_request(request: PullRequestApprovalRequest) -> Any:
    if request.organization is None or request.project is None:
        raise ValueError("Azure DevOps approvals require organization and project")
    return approve_azure_pull_request(
        pull_request_id=request.pull_request_id,
        content=request.content,
        dry_run=request.dry_run,
        config=AzureDevOpsConfig(
            organization=request.organization,
            project=request.project,
            repository=request.repository,
        ),
    )


def _adapter_for(request: PullRequestApprovalRequest) -> PullRequestApprovalAdapter:
    if request.provider == "github":
        return GitHubPullRequestApprovalAdapter()
    return AzureDevOpsPullRequestApprovalAdapter(_approve_azure_request)


def dispatch_pull_request_approval(request: PullRequestApprovalRequest) -> PullRequestApprovalResult:
    """Dispatch one validated request to its provider adapter."""
    try:
        with locked_file(_approval_lock_path(request), mode="a+", timeout=_APPROVAL_LOCK_TIMEOUT_SECONDS):
            return _adapter_for(request).approve(request)
    except SystemExit as exc:
        # The delegated GitHub CLI helpers call sys.exit(1) on readiness failures
        # (missing `gh`, unresolvable current user). SystemExit is not an Exception,
        # so it must be normalized here into a structured result instead of
        # propagating out of the background task uncaught.
        return PullRequestApprovalResult.for_request(
            request, False, "failed", f"provider readiness check exited with code {exc.code}"
        )
    except Exception as exc:
        return PullRequestApprovalResult.for_request(request, False, "failed", _sanitize_diagnostic(exc))


def approve_pull_request(**kwargs: Any) -> dict[str, object]:
    """Approve a pull request using the configured code-hosting provider."""
    request = _build_approval_request(**kwargs)
    result = dispatch_pull_request_approval(request)
    print(json.dumps(result.as_dict(), ensure_ascii=False))
    return result.as_dict()


def _run_request_snapshot(**kwargs: Any) -> int:
    result = dispatch_pull_request_approval(PullRequestApprovalRequest(**kwargs))
    print(json.dumps(result.as_dict(), ensure_ascii=False))
    return 0 if result.success else 1


def approve_pull_request_async(**kwargs: Any) -> None:
    """Snapshot and approve a pull request in a background task."""
    request = _build_approval_request(**kwargs)
    task = run_function_in_background(
        _MODULE,
        "_run_request_snapshot",
        command_display_name="agdt-approve-pull-request",
        args=request.__dict__,
        func_kwargs=request.__dict__,
    )
    print_task_tracking_info(task, "Approving pull request")


def approve_pull_request_async_cli() -> None:
    """CLI entry point for the provider-neutral approval command."""
    parser = argparse.ArgumentParser(description="Approve a pull request")
    parser.add_argument("-p", "--pull-request-id")
    parser.add_argument("-c", "--content")
    parser.add_argument("--provider")
    parser.add_argument("--repo")
    parser.add_argument("--expected-head", "--head-sha", dest="expected_head")
    args = parser.parse_args()
    try:
        approve_pull_request_async(
            provider=args.provider,
            repository=args.repo,
            pull_request_id=args.pull_request_id,
            content=args.content,
            expected_head=args.expected_head,
        )
    except (ValueError, TypeError) as exc:
        parser.error(str(exc))
