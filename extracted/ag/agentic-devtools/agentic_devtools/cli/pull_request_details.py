"""Provider-neutral ``agdt-get-pull-request-details`` command."""

from __future__ import annotations

import argparse
import json
import os
from collections.abc import Mapping
from typing import Any
from uuid import uuid4

from agentic_devtools.adapters.base import is_valid_github_repository
from agentic_devtools.adapters.pull_request_details import (
    _deep_merge_state,
    detect_provider,
    fetch_pull_request_details,
)
from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.cli.azure_devops.helpers import parse_bool_from_state_value
from agentic_devtools.state import (
    get_state_dir,
    is_dry_run,
    load_state_locked,
    read_modify_write_state,
    set_value,
)
from agentic_devtools.task_state import print_task_tracking_info

_OUTPUT_NAME = "temp-get-pull-request-details-response.json"
_ACTIVE_REQUEST_KEY = "_pull_request_details_request_id"


def _state_value(state: Mapping[str, Any], *keys: str) -> object:
    for key in keys:
        current: object = state
        for part in key.split("."):
            if not isinstance(current, Mapping):
                current = None
                break
            current = current.get(part)
        if current is not None:
            return current
    return None


def get_pull_request_details(
    *,
    provider: str | None = None,
    pull_request_id: int | None = None,
    repository: str | None = None,
    state: Mapping[str, Any] | None = None,
    state_snapshot: bool = False,
    request_id: str | None = None,
) -> dict[str, Any] | None:
    """Fetch details, persist a request-scoped artifact, and conditionally update compatibility state.

    Live-state calls record the resolved provider and repository before fetching so
    remotely detected providers can safely publish the compatibility response.
    """
    resolved_state: Mapping[str, Any] | None = state
    used_persisted_fallback = False
    state_for_lookup = state or {}
    stored_provider = _state_value(state_for_lookup, "platform.code_hosting", "provider", "github.provider")
    state_provider = provider or stored_provider
    legacy_repository_key = "github.repo" if str(state_provider).lower() == "github" else "azure_devops.repository"
    canonical_repository = _state_value(state_for_lookup, "sourceCodeHostingPlatform.pullRequest.repository")
    canonical_provider_matches = (
        provider is None or stored_provider is None or str(provider).lower() == str(stored_provider).lower()
    )
    repository_complete = _state_value(state_for_lookup, legacy_repository_key) is not None or (
        canonical_repository is not None and canonical_provider_matches
    )
    if state is None:
        resolved_state = load_state_locked()
        used_persisted_fallback = True
    elif not state_snapshot and (
        (provider is None and _state_value(state, "platform.code_hosting", "provider", "github.provider") is None)
        or (pull_request_id is None and _state_value(state, "pull_request_id", "github.pull_request_number") is None)
        or (repository is None and not repository_complete)
    ):
        resolved_state = _deep_merge_state(load_state_locked(), state)
        used_persisted_fallback = True
    assert resolved_state is not None
    selected = detect_provider(provider, resolved_state, repository)
    raw_pr = (
        pull_request_id
        if pull_request_id is not None
        else _state_value(resolved_state, "pull_request_id", "github.pull_request_number")
    )
    if isinstance(raw_pr, bool) or not isinstance(raw_pr, (int, str)):
        raise SystemExit("pull_request_id must be set to a positive integer")
    try:
        pr_number = int(raw_pr)
    except (TypeError, ValueError) as exc:
        raise SystemExit("pull_request_id must be set to a positive integer") from exc
    if pr_number <= 0:
        raise SystemExit("pull_request_id must be set to a positive integer")
    if repository is not None:
        if not isinstance(repository, str) or not repository.strip():
            raise ValueError("repository override must be a non-empty string")
        if selected == "github" and not is_valid_github_repository(repository):
            raise ValueError("GitHub repository must be in owner/repo form")
    raw_repo: object
    if repository is not None:
        raw_repo = repository
    else:
        resolved_provider = _state_value(resolved_state, "platform.code_hosting", "provider", "github.provider")
        provider_matches_state = (
            provider is None or resolved_provider is None or str(provider).lower() == str(resolved_provider).lower()
        )
    if repository is None and selected == "github":
        canonical_repo = _state_value(resolved_state, "sourceCodeHostingPlatform.pullRequest.repository")
        if (
            provider is not None
            and resolved_provider is not None
            and str(provider).lower() != str(resolved_provider).lower()
        ):
            canonical_repo = None
        github_repo = canonical_repo if canonical_repo is not None else _state_value(resolved_state, "github.repo")
        generic_repo = _state_value(resolved_state, "repository")
        raw_repo = github_repo if isinstance(github_repo, str) and is_valid_github_repository(github_repo) else None
        if (
            raw_repo is None
            and provider_matches_state
            and isinstance(generic_repo, str)
            and is_valid_github_repository(generic_repo)
        ):
            raw_repo = generic_repo
    elif repository is None:
        canonical_repo = _state_value(resolved_state, "sourceCodeHostingPlatform.pullRequest.repository")
        if (
            provider is not None
            and resolved_provider is not None
            and str(provider).lower() != str(resolved_provider).lower()
        ):
            canonical_repo = None
        azure_repo = (
            canonical_repo if canonical_repo is not None else _state_value(resolved_state, "azure_devops.repository")
        )
        raw_repo = (
            azure_repo
            if azure_repo is not None
            else (_state_value(resolved_state, "repository") if provider_matches_state else None)
        )
    repo = raw_repo if isinstance(raw_repo, str) else None
    output_file = get_state_dir() / _OUTPUT_NAME
    if state_snapshot:
        raw_dry_run = _state_value(resolved_state, "dry_run")
        dry_run = parse_bool_from_state_value(raw_dry_run) if raw_dry_run is not None else False
    elif is_dry_run():
        dry_run = True
    elif state is not None and "dry_run" in state:
        dry_run = parse_bool_from_state_value(state.get("dry_run"))
    elif used_persisted_fallback and resolved_state.get("dry_run") is not None:
        dry_run = parse_bool_from_state_value(resolved_state.get("dry_run"))
    else:
        dry_run = False
    if selected == "github" and not repo:
        from agentic_devtools.cli.github.repo_resolution import resolve_github_repo_safe

        repo = resolve_github_repo_safe(resolved_state)
    if selected == "github" and not is_valid_github_repository(repo or "") and (repo is not None or not dry_run):
        raise ValueError("GitHub repository must be in owner/repo form")
    if dry_run:
        repository_scope = repo if repo else "[provider default]"
        print(
            f"DRY-RUN: Would retrieve {selected} pull request details for PR {pr_number} "
            f"in repository {repository_scope}"
        )
        print(f"  Output: {output_file}")
        return None
    generated_request_id = request_id is None and not state_snapshot
    if generated_request_id:
        request_id = uuid4().hex
    if request_id is not None:
        with read_modify_write_state() as current_state:
            if generated_request_id:
                current_state[_ACTIVE_REQUEST_KEY] = request_id
            if generated_request_id or current_state.get(_ACTIVE_REQUEST_KEY) == request_id:
                current_provider = _state_value(current_state, "platform.code_hosting", "provider", "github.provider")
                if isinstance(current_provider, str) and current_provider.lower() != selected:
                    current_state.pop("repository", None)
                    source_hosting = current_state.get("sourceCodeHostingPlatform")
                    if isinstance(source_hosting, dict):
                        pull_request = source_hosting.get("pullRequest")
                        if isinstance(pull_request, dict):
                            pull_request.pop("repository", None)
                    for provider_name, repository_key in (("github", "repo"), ("azure_devops", "repository")):
                        if provider_name != selected:
                            provider_state = current_state.get(provider_name)
                            if isinstance(provider_state, dict):
                                provider_state.pop(repository_key, None)
                context: dict[str, Any] = {
                    "provider": selected,
                    "platform": {"code_hosting": selected},
                    "pull_request_id": pr_number,
                }
                if repo is not None:
                    context["sourceCodeHostingPlatform"] = {"pullRequest": {"repository": repo}}
                    context[selected] = {"repo" if selected == "github" else "repository": repo}
                current_state.update(_deep_merge_state(current_state, context))
    output_file.parent.mkdir(parents=True, exist_ok=True)
    artifact_id = uuid4().hex
    request_artifact = output_file.with_name(f"{output_file.stem}.{selected}.{pr_number}.{artifact_id}.json")
    request_output_file = output_file.with_name(f".{request_artifact.name}.tmp")
    compatibility_temp = output_file.with_name(f".{output_file.name}.{artifact_id}.tmp")
    compatibility_updated = False
    resolved_repository = repo
    try:
        payload = fetch_pull_request_details(
            selected,
            pr_number,
            repo,
            state=resolved_state,
            output_file=request_output_file,
            dry_run=dry_run,
            state_snapshot=state_snapshot,
        )
        if payload is None:
            if not request_output_file.exists():
                raise RuntimeError("Azure DevOps pull-request details command did not produce an output file")
            payload = json.loads(request_output_file.read_text(encoding="utf-8"))
        if resolved_repository is None and selected == "azure_devops":
            raw_resolved_repository = _state_value(payload, "repository.name")
            if isinstance(raw_resolved_repository, str) and raw_resolved_repository.strip():
                resolved_repository = raw_resolved_repository
        request_output_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        os.replace(request_output_file, request_artifact)
        with read_modify_write_state() as current_state:
            current_provider = _state_value(current_state, "platform.code_hosting", "provider", "github.provider")
            current_pr = _state_value(current_state, "pull_request_id", "github.pull_request_number")
            current_repository = _state_value(
                current_state,
                "sourceCodeHostingPlatform.pullRequest.repository",
                "github.repo" if selected == "github" else "azure_devops.repository",
                "repository",
            )
            context_matches = (
                (request_id is None or current_state.get(_ACTIVE_REQUEST_KEY) == request_id)
                and isinstance(current_provider, str)
                and current_provider.lower() == selected
                and not isinstance(current_pr, bool)
                and str(current_pr) == str(pr_number)
                and current_repository == repo
            )
            if context_matches:
                if repo is None and resolved_repository is not None:
                    repository_context = {
                        "sourceCodeHostingPlatform": {"pullRequest": {"repository": resolved_repository}},
                        "azure_devops": {"repository": resolved_repository},
                    }
                    current_state.update(_deep_merge_state(current_state, repository_context))
                compatibility_temp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
                os.replace(compatibility_temp, output_file)
                compatibility_updated = True
    finally:
        request_output_file.unlink(missing_ok=True)
        compatibility_temp.unlink(missing_ok=True)
    print(f"Pull request details written to {request_artifact}")
    if compatibility_updated:
        print(f"Compatibility response updated at {output_file}")
    return payload


def get_pull_request_details_async(
    *,
    provider: str | None = None,
    pull_request_id: int | None = None,
    repository: str | None = None,
) -> None:
    """Queue the provider-neutral pull-request details command.

    ``provider``, ``pull_request_id``, and ``repository`` are forwarded as explicit
    keyword arguments to the background worker so they take precedence over any
    persisted state, including a stale top-level ``provider`` key that would
    otherwise outrank the ``--provider`` override. The worker receives only the
    captured state fields needed for provider, PR, repository, and configuration
    resolution, plus a request ID so queued requests cannot publish over a newer
    request.
    """
    request_id = uuid4().hex
    with read_modify_write_state() as request_state:
        state_dir = str(get_state_dir(create=False).resolve())
        if provider is not None or pull_request_id is not None or repository is not None:
            stored_provider = _state_value(request_state, "platform.code_hosting", "provider", "github.provider")
            selected_provider = detect_provider(provider, request_state, repository)
            if pull_request_id is not None and (
                isinstance(pull_request_id, bool) or not isinstance(pull_request_id, int) or pull_request_id <= 0
            ):
                raise ValueError("pull_request_id must be a positive integer")
            if repository is not None:
                if not isinstance(repository, str) or not repository.strip():
                    raise ValueError("repository override must be a non-empty string")
                if selected_provider == "github" and not is_valid_github_repository(repository):
                    raise ValueError("GitHub repository must be in owner/repo form")
            if isinstance(stored_provider, str) and stored_provider.lower() != selected_provider:
                request_state.pop("repository", None)
                source_hosting = request_state.get("sourceCodeHostingPlatform")
                if isinstance(source_hosting, dict):
                    pull_request = source_hosting.get("pullRequest")
                    if isinstance(pull_request, dict):
                        pull_request.pop("repository", None)
                old_provider_state = request_state.get(
                    "azure_devops" if stored_provider.lower() == "azure_devops" else "github"
                )
                if isinstance(old_provider_state, dict):
                    old_provider_state.pop("repository" if stored_provider.lower() == "azure_devops" else "repo", None)
            request_state["provider"] = selected_provider
            platform = request_state.get("platform")
            if not isinstance(platform, dict):
                platform = {}
                request_state["platform"] = platform
            platform["code_hosting"] = selected_provider
            if repository is not None:
                source_hosting = request_state.get("sourceCodeHostingPlatform")
                if not isinstance(source_hosting, dict):
                    source_hosting = {}
                    request_state["sourceCodeHostingPlatform"] = source_hosting
                pull_request = source_hosting.get("pullRequest")
                if not isinstance(pull_request, dict):
                    pull_request = {}
                    source_hosting["pullRequest"] = pull_request
                pull_request["repository"] = repository
            if pull_request_id is not None:
                request_state["pull_request_id"] = pull_request_id
        request_state[_ACTIVE_REQUEST_KEY] = request_id
    snapshot_keys = (
        "organization",
        "project",
        "repository",
        "pull_request_id",
        "github.pull_request_number",
        "github.repo",
        "dry_run",
        "provider",
        _ACTIVE_REQUEST_KEY,
    )
    worker_state = {key: request_state[key] for key in snapshot_keys if key in request_state}
    for section, keys in (
        ("platform", ("code_hosting",)),
        ("github", ("provider", "repo", "pull_request_number")),
        ("azure_devops", ("organization", "project", "repository")),
    ):
        section_state = request_state.get(section)
        if isinstance(section_state, Mapping):
            selected_values = {key: section_state[key] for key in keys if key in section_state}
            if selected_values:
                worker_state[section] = selected_values
                if section == "azure_devops":
                    for key in ("organization", "project"):
                        top_level_value = worker_state.get(key)
                        if key in selected_values and not (
                            isinstance(top_level_value, str) and top_level_value.strip()
                        ):
                            worker_state[key] = selected_values[key]
    source_hosting = request_state.get("sourceCodeHostingPlatform")
    if isinstance(source_hosting, Mapping):
        pull_request = source_hosting.get("pullRequest")
        if isinstance(pull_request, Mapping) and "repository" in pull_request:
            worker_state["sourceCodeHostingPlatform"] = {"pullRequest": {"repository": pull_request["repository"]}}
    func_kwargs: dict[str, Any] = {
        "state": worker_state,
        "state_snapshot": True,
        "request_id": request_id,
    }
    if provider is not None:
        func_kwargs["provider"] = provider
    if pull_request_id is not None:
        func_kwargs["pull_request_id"] = pull_request_id
    if repository is not None:
        func_kwargs["repository"] = repository
    task = run_function_in_background(
        "agentic_devtools.cli.pull_request_details",
        "get_pull_request_details",
        command_display_name="agdt-get-pull-request-details",
        func_kwargs=func_kwargs or None,
        state_dir=state_dir,
    )
    print_task_tracking_info(task, "Getting pull request details")


def get_pull_request_details_async_cli() -> None:
    """Parse optional provider, repository, and pull-request overrides."""
    parser = argparse.ArgumentParser(description="Get pull request details asynchronously in the background.")
    parser.add_argument("--provider", choices=("azure_devops", "github"))
    parser.add_argument(
        "--pr",
        type=int,
        help="Pull request ID; defaults to the persisted pull_request_id state value when omitted.",
    )
    parser.add_argument("--repo")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Accepted for compatibility; the worker persists the response and logs its output path.",
    )
    args = parser.parse_args()
    if args.pr is not None and args.pr <= 0:
        parser.error("--pr must be a positive integer")
    has_overrides = args.provider is not None or args.repo is not None or args.pr is not None
    persisted_state = load_state_locked() if has_overrides else None
    effective_provider: str | None = None
    inherited_repository: str | None = None
    provider_changed = False
    if persisted_state is not None:
        try:
            effective_provider = detect_provider(args.provider, persisted_state, args.repo)
        except ValueError as exc:
            parser.error(str(exc))
        persisted_provider = _state_value(persisted_state, "platform.code_hosting", "provider", "github.provider")
        canonical_repository = _state_value(persisted_state, "sourceCodeHostingPlatform.pullRequest.repository")
        if persisted_provider is not None and str(persisted_provider).lower() != effective_provider:
            canonical_repository = None
        provider_changed = persisted_provider is not None and str(persisted_provider).lower() != effective_provider
        if effective_provider == "github":
            github_repo = canonical_repository
            if github_repo is None:
                github_repo = _state_value(persisted_state, "github.repo")
            if not provider_changed and (
                not isinstance(github_repo, str) or not is_valid_github_repository(github_repo)
            ):
                github_repo = _state_value(persisted_state, "repository")
            if isinstance(github_repo, str) and is_valid_github_repository(github_repo):
                inherited_repository = github_repo
        else:
            azure_repo = canonical_repository
            if azure_repo is None:
                azure_repo = _state_value(persisted_state, "azure_devops.repository")
            if azure_repo is None and not provider_changed:
                azure_repo = _state_value(persisted_state, "repository")
            if isinstance(azure_repo, str) and azure_repo.strip():
                inherited_repository = azure_repo
    if args.repo is not None and not args.repo.strip():
        parser.error("--repo must be a non-empty string")
    if args.repo is not None and effective_provider == "github" and not is_valid_github_repository(args.repo):
        parser.error("--repo must be in owner/repo form for GitHub")
    if args.pr is not None:
        # The first write may switch the active state directory to PR scope;
        # repeat it so the identifier exists in that resulting scope.
        set_value("pull_request_id", args.pr)
        set_value("pull_request_id", args.pr)
        if persisted_state is not None and "dry_run" in persisted_state:
            set_value("dry_run", persisted_state["dry_run"])
        if effective_provider == "azure_devops":
            azure_state = persisted_state.get("azure_devops") if persisted_state is not None else None
            for key in ("organization", "project"):
                value = None if provider_changed or persisted_state is None else persisted_state.get(key)
                if not (isinstance(value, str) and value.strip()) and isinstance(azure_state, Mapping):
                    value = azure_state.get(key)
                if isinstance(value, str) and value.strip():
                    set_value(key, value)
    dispatch_kwargs: dict[str, Any] = {}
    provider_to_dispatch = args.provider or effective_provider
    if provider_to_dispatch is not None:
        dispatch_kwargs["provider"] = provider_to_dispatch
    if args.pr is not None:
        dispatch_kwargs["pull_request_id"] = args.pr
    repository_to_dispatch = args.repo
    if repository_to_dispatch is None and args.pr is not None:
        repository_to_dispatch = inherited_repository
    if repository_to_dispatch is not None:
        dispatch_kwargs["repository"] = repository_to_dispatch
    get_pull_request_details_async(**dispatch_kwargs)
