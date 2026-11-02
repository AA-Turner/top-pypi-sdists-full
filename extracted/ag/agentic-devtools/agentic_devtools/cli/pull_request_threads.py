"""Provider-neutral background command for resolving pull-request threads."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any

from agentic_devtools.adapters.base import is_valid_github_repository
from agentic_devtools.adapters.pull_request_threads import (
    AzureDevOpsThreadResolutionAdapter,
    GitHubPullRequestThreadsAdapter,
    GitHubThreadResolutionAdapter,
    PullRequestThread,
    PullRequestThreadsRequest,
    ThreadResolutionRequest,
    ThreadResolutionResult,
    sanitize_diagnostic,
)
from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.cli.azure_devops.auth import get_pat
from agentic_devtools.cli.azure_devops.config import (
    DEFAULT_ORGANIZATION,
    DEFAULT_PROJECT,
    AzureDevOpsConfig,
    get_azure_devops_context_from_git_remote,
)
from agentic_devtools.cli.github.repo_resolution import resolve_github_repo_safe
from agentic_devtools.config import load_platform_config, load_repo_config
from agentic_devtools.state import (
    get_repo_root,
    get_value,
    get_workflow_state,
    is_dry_run,
    read_modify_write_state,
    set_value,
)
from agentic_devtools.task_state import print_task_tracking_info

_MODULE = "agentic_devtools.cli.pull_request_threads"
_PROVIDERS = frozenset({"azure_devops", "github"})
_ADO_ORG_URL = re.compile(
    r"^https://(?:dev\.azure\.com/[A-Za-z0-9][A-Za-z0-9._-]*|[A-Za-z0-9][A-Za-z0-9._-]*\.visualstudio\.com)/?$"
)
_ADO_ORG_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def _state_or(value: object, *keys: str) -> object:
    """Return an explicit value or the first value found in state."""
    if value is not None:
        return value
    for key in keys:
        found = get_value(key)
        if found is not None:
            return found
    return None


def _none_if_blank(value: object) -> object:
    """Treat blank string aliases as an absent value."""
    if isinstance(value, str) and not value.strip():
        return None
    return value


def resolve_thread_provider(
    provider: str | None = None,
    *,
    allow_legacy_azure_fallback: bool = False,
) -> str:
    """Select a configured provider, optionally falling back to legacy Azure configuration."""
    configured: object = provider if provider is not None else get_value("platform.code_hosting")
    if provider is None and configured == "other":
        configured = None
    root_config: dict[str, Any] | None = None
    if configured is None:
        workflow = get_workflow_state()
        context = workflow.get("context") if isinstance(workflow, dict) else None
        if isinstance(context, dict):
            configured = context.get("code_hosting") or context.get("platform_code_hosting")
    if configured is None:
        root = get_repo_root()
        if root is not None:
            configured = load_platform_config(str(root)).get("code_hosting")
            if configured == "other":
                root_config = load_repo_config(str(root))
                platform_config = root_config.get("platform")
                if platform_config is None or (
                    isinstance(platform_config, dict) and "code_hosting" not in platform_config
                ):
                    configured = None
    if not isinstance(configured, str) or configured not in _PROVIDERS:
        if configured is None and allow_legacy_azure_fallback:
            remote_context = get_azure_devops_context_from_git_remote()
            platform_config = root_config.get("platform") if root_config is not None else None
            azure_config = platform_config.get("azure_devops") if isinstance(platform_config, dict) else None
            azure_values = (
                get_value("organization"),
                get_value("project"),
                azure_config.get("organization") if isinstance(azure_config, dict) else None,
                azure_config.get("project") if isinstance(azure_config, dict) else None,
            )
            if remote_context is not None or any(
                isinstance(value, str)
                and value.strip()
                and value.strip() not in {DEFAULT_ORGANIZATION, DEFAULT_PROJECT}
                for value in azure_values
            ):
                return "azure_devops"
        raise ValueError("platform.code_hosting must be 'azure_devops' or 'github'")
    return configured


def _positive_int(value: object, name: str) -> int | None:
    """Parse an optional positive integer without coercing arbitrary objects."""
    if value is None or value == "":
        return None
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        raise ValueError(f"{name} must be a positive integer")
    try:
        number = int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a positive integer") from exc
    if number <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return number


def _repository(provider: str, explicit: str | None) -> str:
    """Resolve repository identity without consulting credentials."""
    if provider == "github":
        value = _state_or(explicit, "github.repo")
        if value is not None and not isinstance(value, str):
            raise ValueError(
                f"github.repo must be a string, got {type(value).__name__!r}; "
                "use agdt-set to store an owner/repo string"
            )
        if value is None:
            legacy_repository = get_value("repository")
            if isinstance(legacy_repository, str) and is_valid_github_repository(legacy_repository.strip()):
                value = legacy_repository
        normalized = value.strip() if isinstance(value, str) and value.strip() else None
        if normalized is None:
            root = get_repo_root()
            configured = None
            if root is not None:
                github_config = load_platform_config(str(root)).get("github")
                if isinstance(github_config, dict):
                    configured = github_config.get("repo")
                    if configured is not None and not isinstance(configured, str):
                        raise ValueError("platform.github.repo must be a string")
            normalized = (
                os.environ.get("GITHUB_REPOSITORY", "").strip()
                or (configured.strip() if isinstance(configured, str) and configured.strip() else None)
                or resolve_github_repo_safe()
            )
        if not isinstance(normalized, str) or not normalized.strip():
            raise ValueError("repository is required")
        normalized = normalized.strip()
        if not is_valid_github_repository(normalized):
            raise ValueError("GitHub repository must be in owner/repo form")
        return normalized
    value = _state_or(explicit, "repository")
    if not isinstance(value, str) or not value.strip():
        raise ValueError("repository is required")
    return value.strip()


def _validate_azure_devops_organization(value: str) -> str:
    """Normalize plain org names and reject non-Azure URLs."""
    if "://" not in value:
        if not _ADO_ORG_NAME.match(value):
            raise ValueError(
                "organization must be a plain org name or a 'https://dev.azure.com/<org>' / "
                "'https://<org>.visualstudio.com' URL"
            )
        return f"https://dev.azure.com/{value}"
    if not _ADO_ORG_URL.match(value):
        raise ValueError(
            "organization must be a plain org name or a 'https://dev.azure.com/<org>' / "
            "'https://<org>.visualstudio.com' URL"
        )
    return value


def _azure_devops_context(
    explicit_repository: str | None = None,
    *,
    explicit_organization: str | None = None,
    explicit_project: str | None = None,
) -> tuple[str, str, str]:
    """Resolve Azure DevOps coordinates from explicit inputs, state, config, or remote."""
    for name, value in (
        ("repository", explicit_repository),
        ("organization", explicit_organization),
        ("project", explicit_project),
    ):
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError(f"{name} must be a non-empty string")
    organization = _state_or(explicit_organization, "organization")
    project = _state_or(explicit_project, "project")
    repository = explicit_repository if explicit_repository is not None else _state_or(None, "repository")

    normalized_organization = organization.strip() if isinstance(organization, str) and organization.strip() else None
    if normalized_organization is not None:
        normalized_organization = _validate_azure_devops_organization(normalized_organization)
    normalized_project = project.strip() if isinstance(project, str) and project.strip() else None
    normalized_repository = repository.strip() if isinstance(repository, str) and repository.strip() else None

    if normalized_organization is None or normalized_project is None or normalized_repository is None:
        root = get_repo_root()
        root_azure_config = load_platform_config(str(root)).get("azure_devops") if root is not None else {}
        if not isinstance(root_azure_config, dict):
            root_azure_config = {}
        if normalized_organization is None:
            configured_organization = root_azure_config.get("organization")
            if isinstance(configured_organization, str) and configured_organization.strip():
                normalized_organization = _validate_azure_devops_organization(configured_organization.strip())
        if normalized_project is None:
            configured_project = root_azure_config.get("project")
            if isinstance(configured_project, str) and configured_project.strip():
                normalized_project = configured_project.strip()
        if normalized_repository is None:
            configured_repository = root_azure_config.get("repository")
            if isinstance(configured_repository, str) and configured_repository.strip():
                normalized_repository = configured_repository.strip()

    if normalized_organization is not None and normalized_project is not None and normalized_repository is not None:
        return normalized_organization, normalized_project, normalized_repository

    remote_context = get_azure_devops_context_from_git_remote()
    remote_organization = remote_context[0] if remote_context else None
    remote_project = remote_context[1] if remote_context else None
    remote_repository = remote_context[2] if remote_context else None

    if normalized_organization is None:
        normalized_organization = remote_organization
    if normalized_project is None:
        normalized_project = remote_project
    if normalized_repository is None:
        normalized_repository = remote_repository
    if normalized_organization is None or normalized_project is None or normalized_repository is None:
        raise ValueError("Azure DevOps organization, project, and repository are required")
    return normalized_organization, normalized_project, normalized_repository


def build_thread_resolution_request(
    *,
    provider: str | None = None,
    repository: str | None = None,
    pull_request_id: str | int | None = None,
    thread_id: str | int | None = None,
    thread_node_id: str | None = None,
    comment_id: str | int | None = None,
    dry_run: bool | None = None,
) -> ThreadResolutionRequest:
    """Validate state/CLI inputs and create one immutable request snapshot."""
    if dry_run is not None and not isinstance(dry_run, bool):
        raise ValueError("dry_run must be a boolean")
    selected = resolve_thread_provider(provider)
    pr_number = _positive_int(
        _state_or(pull_request_id, "pull_request_id", "github.pull_request_number", "pr_number"),
        "pull_request_id",
    )
    if pr_number is None:
        raise ValueError("pull_request_id is required")

    explicit_identifier = thread_id is not None or thread_node_id is not None or comment_id is not None
    raw_thread: object
    raw_node: object
    raw_comment: object
    if explicit_identifier:
        raw_thread = thread_id
        raw_node = thread_node_id
        raw_comment = comment_id
    elif selected == "github":
        raw_thread = _none_if_blank(_state_or(None, "thread_id"))
        raw_node = _none_if_blank(_state_or(None, "github.thread_node_id", "github.review_thread_id", "thread_node_id"))
        raw_comment = _none_if_blank(_state_or(None, "github.comment_id", "comment_id"))
        if raw_node is not None:
            raw_comment = None
            raw_thread = None
        elif raw_comment is not None:
            raw_thread = None
    else:
        raw_thread = _state_or(None, "thread_id")
        raw_node = None
        raw_comment = None
    if raw_thread is not None:
        if raw_node is not None or raw_comment is not None:
            raise ValueError("thread_id cannot be combined with thread_node_id or comment_id")
        if selected == "azure_devops":
            raw_ado = raw_thread
            raw_node = None
            raw_comment = None
        elif isinstance(raw_thread, int) or (isinstance(raw_thread, str) and raw_thread.isdigit()):
            raw_comment = raw_thread
            raw_ado = None
        else:
            raw_node = raw_thread
            raw_ado = None
    else:
        raw_ado = raw_thread if selected == "azure_devops" else None

    ado_id = _positive_int(raw_ado, "azure_devops_thread_id") if selected == "azure_devops" else None
    github_comment = _positive_int(raw_comment, "github_comment_id") if selected == "github" else None
    if selected == "github" and raw_node is not None and not isinstance(raw_node, str):
        raise ValueError("thread_node_id must be a string")
    if selected == "github" and raw_node is None and github_comment is None:
        raise ValueError("thread_id, thread_node_id, or comment_id is required")
    if selected == "azure_devops" and ado_id is None:
        raise ValueError("thread_id is required")

    azure_organization = None
    azure_project = None
    if selected == "azure_devops":
        azure_organization, azure_project, repository_value = _azure_devops_context(repository)
    else:
        repository_value = _repository(selected, repository)

    return ThreadResolutionRequest(
        provider=selected,
        repository=repository_value,
        pull_request_id=pr_number,
        azure_devops_thread_id=ado_id,
        azure_devops_organization=azure_organization,
        azure_devops_project=azure_project,
        github_thread_node_id=raw_node if isinstance(raw_node, str) and selected == "github" else None,
        github_comment_id=github_comment,
        dry_run=is_dry_run() if dry_run is None else dry_run,
    )


def _adapter_for(request: ThreadResolutionRequest) -> Any:  # pragma: no cover
    """Create only the adapter selected by the immutable request."""
    if request.provider == "github":
        return GitHubThreadResolutionAdapter()
    if request.azure_devops_organization is None or request.azure_devops_project is None:
        raise ValueError("Azure DevOps request snapshot must include organization and project")
    config = AzureDevOpsConfig(
        request.azure_devops_organization,
        request.azure_devops_project,
        request.repository,
    )
    try:
        pat = get_pat() if not request.dry_run else ""
    except Exception:
        pat = ""
    return AzureDevOpsThreadResolutionAdapter(config, pat)


def dispatch_thread_resolution(request: ThreadResolutionRequest) -> ThreadResolutionResult:
    """Run one request without provider fallback."""
    try:
        return _adapter_for(request).resolve(request)
    except Exception as exc:
        return ThreadResolutionResult(
            False,
            request.provider,
            request.repository,
            request.pull_request_id,
            status="failed",
            diagnostics=(sanitize_diagnostic(exc),),
            azure_devops_thread_id=request.azure_devops_thread_id,
            github_thread_node_id=request.github_thread_node_id,
            github_comment_id=request.github_comment_id,
        )


def resolve_thread(**kwargs: Any) -> ThreadResolutionResult:
    """Resolve a thread synchronously and persist the structured result."""
    try:
        has_request = "request" in kwargs
        request_data = kwargs.pop("request", None)
        if has_request:
            if not isinstance(request_data, dict):
                raise ValueError("request snapshot must be a dictionary")
            request = ThreadResolutionRequest(**request_data)
        else:
            request = build_thread_resolution_request(**kwargs)
    except Exception as exc:
        result = ThreadResolutionResult(
            False, str(kwargs.get("provider") or "unknown"), "", 0, status="invalid", diagnostics=(str(exc)[:1000],)
        )
    else:
        result = dispatch_thread_resolution(request)
    with read_modify_write_state() as state:
        state["thread_resolution_result"] = result.as_dict()
    print(json.dumps(result.as_dict(), ensure_ascii=False))
    return result


def resolve_thread_async(
    pull_request_id: str | None = None,
    thread_id: str | None = None,
    provider: str | None = None,
    repository: str | None = None,
    thread_node_id: str | None = None,
    comment_id: str | None = None,
    dry_run: bool | None = None,
) -> None:
    """Snapshot and validate one request before starting a background task."""
    if len(sys.argv) > 1 and all(
        value is None
        for value in (pull_request_id, thread_id, provider, repository, thread_node_id, comment_id, dry_run)
    ):
        parser = argparse.ArgumentParser(description="Resolve a pull request discussion")
        parser.add_argument("-p", "--pull-request-id")
        parser.add_argument("-t", "--thread-id")
        parser.add_argument("--provider")
        parser.add_argument("--repo", "--repository", dest="repository")
        parser.add_argument("--thread-node-id")
        parser.add_argument("--comment-id")
        parser.add_argument("--dry-run", action="store_true", default=None)
        args = parser.parse_args()
        pull_request_id = args.pull_request_id
        thread_id = args.thread_id
        provider = args.provider
        repository = args.repository
        thread_node_id = args.thread_node_id
        comment_id = args.comment_id
        dry_run = args.dry_run
    try:
        request = build_thread_resolution_request(
            provider=provider,
            repository=repository,
            pull_request_id=pull_request_id,
            thread_id=thread_id,
            thread_node_id=thread_node_id,
            comment_id=comment_id,
            dry_run=dry_run,
        )
    except Exception as exc:
        print(json.dumps({"success": False, "status": "invalid", "diagnostics": [str(exc)[:1000]]}))
        raise SystemExit(1) from exc
    task = run_function_in_background(
        _MODULE,
        "_resolve_thread_task",
        command_display_name="agdt-resolve-thread",
        args=request.as_dict(),
        func_kwargs={"request": request.as_dict()},
    )
    print_task_tracking_info(task, "Resolving pull request thread")


def _resolve_thread_task(**kwargs: Any) -> int:
    """Run a snapshot and propagate resolution failure through task status."""
    return 0 if resolve_thread(**kwargs).success else 1


def resolve_thread_async_cli() -> None:  # pragma: no cover
    """Compatibility entry point for callers importing the async command."""
    resolve_thread_async()


def _thread_listing_repository(provider: str) -> str:
    """Read the repository key used by the selected provider."""
    return _repository(provider, None)


def get_pull_request_threads(
    pull_request_id: str | int | None = None,
    *,
    provider: str | None = None,
    repository: str | None = None,
    organization: str | None = None,
    project: str | None = None,
) -> tuple[PullRequestThread, ...] | None:
    """Print pull-request threads using provider coordinates from state, config, or remote."""
    selected_provider = resolve_thread_provider(provider, allow_legacy_azure_fallback=True)
    raw_id = pull_request_id if pull_request_id is not None else get_value("pull_request_id")
    if not isinstance(raw_id, (str, int)) or isinstance(raw_id, bool):
        raise ValueError("pull_request_id must be a positive integer")
    try:
        pr_number = int(raw_id)
    except ValueError as exc:
        raise ValueError("pull_request_id must be a positive integer") from exc
    if pr_number <= 0:
        raise ValueError("pull_request_id must be a positive integer")
    if selected_provider == "azure_devops":
        from agentic_devtools.cli.azure_devops.commands import get_pull_request_threads as get_azure_threads

        azure_organization, azure_project, azure_repository = _azure_devops_context(
            repository,
            explicit_organization=organization,
            explicit_project=project,
        )
        get_azure_threads(
            pr_number,
            repository=azure_repository,
            organization=azure_organization,
            project=azure_project,
        )
        return None
    repository_value = repository if repository is not None else _thread_listing_repository(selected_provider)
    request = PullRequestThreadsRequest(selected_provider, repository_value, pr_number)
    if is_dry_run():
        print(f"[DRY RUN] Would get threads for PR {request.pull_request_id}")
        print(f"Repository: {request.repository}")
        return None
    threads = GitHubPullRequestThreadsAdapter().list(request)
    print(
        json.dumps(
            [
                {
                    "id": thread.id,
                    "status": thread.status,
                    "file": thread.file,
                    "line": thread.line,
                    "comments": list(thread.comments),
                }
                for thread in threads
            ],
            ensure_ascii=False,
        )
    )
    return threads


def get_pull_request_threads_async(
    pull_request_id: str | None = None,
    provider: str | None = None,
    repository: str | None = None,
) -> None:
    """Run provider-neutral pull-request thread enumeration in the background."""
    if len(sys.argv) > 1 and all(value is None for value in (pull_request_id, provider, repository)):
        parser = argparse.ArgumentParser(description="Get pull request threads")
        parser.add_argument("-p", "--pull-request-id")
        parser.add_argument("--provider")
        parser.add_argument("--repo", "--repository", dest="repository")
        args = parser.parse_args()
        pull_request_id = args.pull_request_id
        provider = args.provider
        repository = args.repository
    try:
        request_id = _positive_int(
            pull_request_id if pull_request_id is not None else get_value("pull_request_id"),
            "pull_request_id",
        )
        if request_id is None:
            raise ValueError("pull_request_id is required")
        selected_provider = resolve_thread_provider(provider, allow_legacy_azure_fallback=True)
        organization = None
        project = None
        if repository is not None:
            if selected_provider == "azure_devops":
                organization, project, repository_value = _azure_devops_context(repository)
            else:
                repository_value = _repository(selected_provider, repository)
        elif selected_provider == "azure_devops":
            organization, project, repository_value = _azure_devops_context()
        else:
            repository_value = _thread_listing_repository(selected_provider)
        if pull_request_id is not None:
            set_value("pull_request_id", request_id)
        task_arguments: dict[str, Any] = {
            "pull_request_id": request_id,
            "provider": selected_provider,
            "repository": repository_value,
        }
        if organization is not None and project is not None:
            task_arguments.update({"organization": organization, "project": project})
        task = run_function_in_background(
            _MODULE,
            "_get_pull_request_threads_task",
            command_display_name="agdt-get-pull-request-threads",
            args=task_arguments,
            func_kwargs=task_arguments.copy(),
        )
    except Exception as exc:
        print(json.dumps({"success": False, "status": "invalid", "diagnostics": [str(exc)[:1000]]}))
        raise SystemExit(1) from exc
    print_task_tracking_info(task, "Getting pull request threads")


def _get_pull_request_threads_task(
    pull_request_id: str | int,
    provider: str,
    repository: str,
    organization: str | None = None,
    project: str | None = None,
) -> int:
    """Run thread enumeration and propagate failures through task status."""
    get_pull_request_threads(
        pull_request_id,
        provider=provider,
        repository=repository,
        organization=organization,
        project=project,
    )
    return 0


__all__ = [
    "build_thread_resolution_request",
    "dispatch_thread_resolution",
    "resolve_thread",
    "resolve_thread_async",
    "resolve_thread_async_cli",
    "resolve_thread_provider",
    "get_pull_request_threads",
    "get_pull_request_threads_async",
]
