"""Provider-neutral pull-request publish command."""

from __future__ import annotations

import os
import sys
from typing import Any

from agentic_devtools.adapters.pull_request_publish import (
    GitHubPullRequestPublishAdapter,
    PullRequestPublishRequest,
    PullRequestPublishResult,
)
from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.cli.azure_devops.helpers import parse_bool_from_state_value
from agentic_devtools.cli.github.repo_resolution import resolve_github_repo_safe
from agentic_devtools.config import load_platform_config, load_repo_config
from agentic_devtools.state import get_repo_root, get_value, is_dry_run
from agentic_devtools.task_state import print_task_tracking_info

_MODULE = "agentic_devtools.cli.pull_request_publish"


def _validated_provider(value: object, source: str) -> str:
    """Return a supported provider name from explicit input or external configuration."""
    if not isinstance(value, str):
        raise ValueError(f"{source} must be 'azure_devops' or 'github'")
    selected = value.strip()
    if selected not in {"azure_devops", "github"}:
        raise ValueError(f"{source} must be 'azure_devops' or 'github'")
    return selected


def _provider(provider: str | None = None) -> str:
    """Resolve the configured code-hosting provider."""
    if provider is not None:
        return _validated_provider(provider, "provider")
    selected = get_value("platform.code_hosting")
    if selected == "other":
        selected = None
    if selected is None:
        root = get_repo_root()
        if root is None:
            return "azure_devops"
        raw_platform = load_repo_config(str(root)).get("platform")
        if raw_platform is None or (isinstance(raw_platform, dict) and "code_hosting" not in raw_platform):
            return "azure_devops"
        selected = load_platform_config(str(root)).get("code_hosting")
    return _validated_provider(selected, "platform.code_hosting")


def _positive_int(value: object, name: str) -> int:
    """Validate a pull-request number."""
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError(f"{name} must be a positive integer")
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a positive integer") from exc
    if result <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return result


def _dry_run_flag(dry_run: bool | None = None) -> bool:
    """Resolve a dry-run override or fall back to the current state."""
    if dry_run is None:
        return is_dry_run()
    if not isinstance(dry_run, bool):
        raise ValueError("dry_run must be a boolean")
    return dry_run


def _github_request(
    provider: str,
    pull_request_id: int | str | None,
    repository: str | None,
    dry_run: bool,
) -> PullRequestPublishRequest:
    """Build a validated GitHub publish request from state and overrides."""
    raw_id = pull_request_id if pull_request_id is not None else get_value("pull_request_id")
    if raw_id is None:
        raw_id = get_value("github.pull_request_number")
    if raw_id is None:
        raise ValueError("pull_request_id is required")
    repo = repository
    if repo is not None and not isinstance(repo, str):
        raise ValueError("repository must be a string")
    if not isinstance(repo, str) or not repo.strip():
        repo = get_value("github.repo")
    if repo is not None and not isinstance(repo, str):
        raise ValueError("github.repo must be a string")
    if not isinstance(repo, str) or not repo.strip():
        repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not isinstance(repo, str) or not repo.strip():
        root = get_repo_root()
        if root is not None:
            github_config = load_platform_config(str(root)).get("github")
            if isinstance(github_config, dict):
                configured_repo = github_config.get("repo")
                if configured_repo is not None and not isinstance(configured_repo, str):
                    raise ValueError("platform.github.repo must be a string")
                repo = configured_repo
    if not isinstance(repo, str) or not repo.strip():
        repo = resolve_github_repo_safe()
    if not isinstance(repo, str) or not repo.strip():
        raise ValueError("repository is required")
    return PullRequestPublishRequest(provider, _positive_int(raw_id, "pull_request_id"), repo.strip(), dry_run)


def publish_pull_request(
    provider: str | None = None,
    repository: str | None = None,
    pull_request_id: int | str | None = None,
    dry_run: bool | None = None,
    skip_auto_complete: bool | None = None,
) -> PullRequestPublishResult | None:
    """Publish a pull request using the configured provider."""
    selected = _provider(provider)
    resolved_dry_run = _dry_run_flag(dry_run)
    if selected == "azure_devops":
        from agentic_devtools.cli.azure_devops.commands import publish_pull_request as publish_azure

        resolved_pull_request_id = (
            pull_request_id if pull_request_id is not None else get_value("pull_request_id", required=True)
        )
        resolved_pull_request_id = _positive_int(resolved_pull_request_id, "pull_request_id")
        publish_azure(
            dry_run=resolved_dry_run,
            pull_request_id=resolved_pull_request_id,
            skip_auto_complete=skip_auto_complete,
        )
        return None
    request = _github_request(selected, pull_request_id, repository, resolved_dry_run)
    result = GitHubPullRequestPublishAdapter().publish(request)
    if result.status == "dry_run":
        print(f"Dry run: PR {request.pull_request_id} would be published.")
    elif result.success:
        print(f"PR {request.pull_request_id} published successfully.")
    else:
        print(f"Error publishing PR: {result.error}", file=sys.stderr)
    return result


def _run_publish(**kwargs: Any) -> int:
    """Run a provider-neutral publish request in a background task."""
    result = publish_pull_request(**kwargs)
    return 0 if result is None or result.success else 1


def publish_pull_request_async(
    provider: str | None = None,
    repository: str | None = None,
    pull_request_id: int | str | None = None,
    dry_run: bool | None = None,
) -> None:
    """Snapshot publish inputs and run the command in the background."""
    selected = _provider(provider)
    resolved_dry_run = _dry_run_flag(dry_run)
    kwargs: dict[str, Any] = {
        "provider": selected,
        "repository": repository,
        "pull_request_id": pull_request_id,
        "dry_run": resolved_dry_run,
    }
    if selected == "github":
        request = _github_request(selected, pull_request_id, repository, resolved_dry_run)
        kwargs["repository"] = request.repository
        kwargs["pull_request_id"] = request.pull_request_id
    else:
        resolved_pull_request_id = (
            pull_request_id if pull_request_id is not None else get_value("pull_request_id", required=True)
        )
        kwargs["pull_request_id"] = _positive_int(resolved_pull_request_id, "pull_request_id")
        kwargs["skip_auto_complete"] = parse_bool_from_state_value(get_value("skip_auto_complete"), default=False)
    task = run_function_in_background(
        _MODULE,
        "_run_publish",
        command_display_name="agdt-publish-pull-request",
        func_kwargs=kwargs,
    )
    print_task_tracking_info(task, "Publishing pull request")
