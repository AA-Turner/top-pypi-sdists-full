"""Provider-neutral pull-request creation command."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any, TypedDict

from agentic_devtools.adapters.pull_request_create import (
    AzureDevOpsPullRequestCreateAdapter,
    GitHubPullRequestCreateAdapter,
    PullRequestCreateAdapter,
    PullRequestCreateRequest,
    PullRequestCreateResult,
)
from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.cli.azure_devops.helpers import convert_to_pull_request_title
from agentic_devtools.cli.pr_template import resolve_pr_body, resolve_pr_title
from agentic_devtools.config import VALID_CODE_HOSTING, load_platform_config, load_repo_config
from agentic_devtools.state import get_repo_root, get_state_dir, get_value, is_dry_run, set_value
from agentic_devtools.task_state import print_task_tracking_info

_PROVIDERS = frozenset({"azure_devops", "github"})
_MODULE = "agentic_devtools.cli.pull_request_create"
_SNAPSHOT_DIR_NAME = "pending-pr-requests"


class _CreateRequestSnapshot(TypedDict):
    provider: str
    source_branch: str
    title: str
    body: str
    body_is_explicit: bool
    target_branch: str
    draft: bool
    reviewers: tuple[str, ...]
    dry_run: bool


def _resolve_configured_provider() -> str | None:
    """Resolve the explicitly configured code-hosting provider, if any.

    Returns ``None`` when neither state nor repository config designates
    ``azure_devops`` or ``github`` explicitly (i.e. the setting is unset or
    ``other``), so callers can distinguish "no opinion" from "explicitly
    configured".
    """
    selected = get_value("platform.code_hosting")
    if isinstance(selected, str) and selected in _PROVIDERS:
        return selected
    if selected not in (None, "other"):
        raise ValueError("platform.code_hosting must be 'azure_devops' or 'github'")

    root = get_repo_root()
    repo_path = str(root or os.getcwd())
    raw_platform = load_repo_config(repo_path).get("platform")
    if isinstance(raw_platform, dict) and "code_hosting" in raw_platform:
        raw_provider = raw_platform["code_hosting"]
        if not isinstance(raw_provider, str) or raw_provider not in VALID_CODE_HOSTING:
            raise ValueError("repository platform.code_hosting must be 'azure_devops' or 'github'")

    configured = load_platform_config(repo_path).get("code_hosting")
    if isinstance(configured, str) and configured in _PROVIDERS:
        return configured
    if configured in (None, "other"):
        return None
    raise ValueError("repository platform.code_hosting must be 'azure_devops' or 'github'")


def resolve_create_provider(provider: str | None = None) -> str:
    """Resolve the configured or explicitly selected code-hosting provider.

    An explicit ``provider`` override is rejected when it disagrees with an
    explicitly configured ``platform.code_hosting`` (state or repository
    config). If no provider is configured, the explicit choice is returned;
    the caller persists it to state after request validation so follow-up PR
    commands use the same provider.
    """
    if provider is not None:
        if not isinstance(provider, str) or provider not in _PROVIDERS:
            raise ValueError("--provider must be 'azure_devops' or 'github'")
        configured = _resolve_configured_provider()
        if configured is None:
            return provider
        if configured != provider:
            raise ValueError(
                f"--provider {provider!r} conflicts with the configured "
                f"platform.code_hosting ({configured!r}); follow-up PR commands "
                "(threads, comments, autofix) would still target the configured "
                "provider. Update platform.code_hosting instead of overriding "
                "--provider for this PR."
            )
        return provider

    configured = _resolve_configured_provider()
    return configured if configured is not None else "azure_devops"


def _as_bool(value: object, default: bool = True) -> bool:
    """Parse the state representation used by existing PR commands."""
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).lower() not in {"0", "false", "no", "off"}


def _state_or(value: object, key: str) -> object:
    return value if value is not None else get_value(key)


def _build_create_request_snapshot(
    *,
    provider: str | None = None,
    source_branch: str | None = None,
    title: str | None = None,
    body: str | None = None,
    target_branch: str | None = None,
    draft: bool | None = None,
    reviewers: str | tuple[str, ...] | list[str] | None = None,
    dry_run: bool | None = None,
) -> _CreateRequestSnapshot:
    """Resolve one immutable request snapshot from CLI overrides and state."""
    selected = resolve_create_provider(provider)
    source = _state_or(source_branch, "source_branch")
    resolved_title = _state_or(title, "title")
    body_is_explicit = body is not None
    description = body if body_is_explicit else get_value("description")
    if not body_is_explicit and description is not None:
        body_is_explicit = True
    target = _state_or(target_branch, "target_branch")
    raw_draft = _state_or(draft, "draft")
    raw_reviewers = _state_or(reviewers, "reviewers")
    if not isinstance(source, str) or not source.strip():
        raise ValueError("source_branch is required")
    source = source.strip()
    if not isinstance(resolved_title, str) or not resolved_title.strip():
        raise ValueError("title is required")
    if description is None:
        description = resolve_pr_body()
    elif not isinstance(description, str):  # pragma: no cover - guarded by _preflight_validate_create_request
        raise ValueError("body must be a string")
    if target is None or (target_branch is None and target == ""):
        resolved_target = "main"
    elif not isinstance(target, str):  # pragma: no cover - guarded by _preflight_validate_create_request
        raise ValueError("target_branch must be a string")
    else:
        resolved_target = target
    if raw_reviewers is None:
        reviewer_values: tuple[str, ...] = ()
    elif isinstance(raw_reviewers, str):
        reviewer_values = tuple(item.strip() for item in raw_reviewers.split(",") if item.strip())
        if not reviewer_values:
            raise ValueError("reviewers must include at least one non-empty name")
    elif isinstance(raw_reviewers, (tuple, list)):
        normalized_reviewers: list[str] = []
        for reviewer_group in raw_reviewers:
            if not isinstance(reviewer_group, str):
                raise ValueError("reviewers must be a comma-separated string or a list/tuple of non-empty strings")
            if not reviewer_group.strip():
                raise ValueError("reviewers must be a list/tuple of non-empty strings")
            group_reviewers = tuple(item.strip() for item in reviewer_group.split(",") if item.strip())
            if not group_reviewers:
                raise ValueError("reviewers must include at least one non-empty name")
            normalized_reviewers.extend(group_reviewers)
        reviewer_values = tuple(normalized_reviewers)
        if not reviewer_values:
            raise ValueError("reviewers must include at least one non-empty name")
    else:  # pragma: no cover - guarded by _preflight_validate_create_request
        raise ValueError("reviewers must be a comma-separated string or a list/tuple of non-empty strings")
    if draft is None:
        resolved_draft = _as_bool(raw_draft)
    elif isinstance(draft, bool):
        resolved_draft = draft
    else:
        raise ValueError("draft must be a boolean")
    if selected == "azure_devops":
        title_template_input = resolved_title if title is not None else None
        resolved_title_str = resolve_pr_title(title_template_input) or convert_to_pull_request_title(resolved_title)
    else:
        resolved_title_str = convert_to_pull_request_title(resolved_title)
    return {
        "provider": selected,
        "source_branch": source,
        "title": resolved_title_str,
        "body": description,
        "body_is_explicit": body_is_explicit,
        "target_branch": resolved_target,
        "draft": resolved_draft,
        "reviewers": reviewer_values,
        "dry_run": is_dry_run() if dry_run is None else dry_run,
    }


def build_create_request(
    *,
    provider: str | None = None,
    source_branch: str | None = None,
    title: str | None = None,
    body: str | None = None,
    target_branch: str | None = None,
    draft: bool | None = None,
    reviewers: str | tuple[str, ...] | list[str] | None = None,
    dry_run: bool | None = None,
) -> PullRequestCreateRequest:
    """Build and validate a request from CLI overrides and state."""
    return PullRequestCreateRequest(
        **_build_create_request_snapshot(
            provider=provider,
            source_branch=source_branch,
            title=title,
            body=body,
            target_branch=target_branch,
            draft=draft,
            reviewers=reviewers,
            dry_run=dry_run,
        )
    )


def _preflight_validate_create_request(
    *,
    provider: str | None = None,
    source_branch: str | None = None,
    title: str | None = None,
    body: str | None = None,
    target_branch: str | None = None,
    draft: bool | None = None,
    reviewers: str | tuple[str, ...] | list[str] | None = None,
    dry_run: bool | None = None,
) -> None:
    """Validate request fields/provider before scheduling the background task.

    Mirrors the structural checks in ``build_create_request()``/
    ``PullRequestCreateRequest`` (required fields, provider, and optional
    value types) so an invalid invocation raises immediately instead of only
    failing later inside ``_run_request_snapshot()``, matching the legacy
    async command's synchronous validation. Optional fields are resolved
    through ``_state_or()`` -- the same fallback ``build_create_request()``
    uses -- so a bad value already sitting in state (not just an explicit
    CLI override) is still caught here. ``draft``/``dry_run`` are the
    exception: both flow through permissive bool coercions
    (``_as_bool()``/``is_dry_run()``) downstream that never raise, so only
    their *explicit* argument form is type-checked here. Body template
    rendering (``resolve_pr_body()``) reads git/state and is performed
    synchronously while the immutable request snapshot is built, before the
    background task is scheduled. Azure DevOps title templates are also
    resolved synchronously; GitHub titles bypass that template.
    """
    resolve_create_provider(provider)
    resolved_source = _state_or(source_branch, "source_branch")
    if not isinstance(resolved_source, str) or not resolved_source.strip():
        raise ValueError("source_branch is required")
    resolved_title = _state_or(title, "title")
    if not isinstance(resolved_title, str) or not resolved_title.strip():
        raise ValueError("title is required")
    resolved_body = _state_or(body, "description")
    if resolved_body is not None and not isinstance(resolved_body, str):
        raise ValueError("body must be a string")
    resolved_target_branch = _state_or(target_branch, "target_branch")
    if target_branch is None and resolved_target_branch == "":
        resolved_target_branch = None
    if resolved_target_branch is not None and (
        not isinstance(resolved_target_branch, str) or not resolved_target_branch.strip()
    ):
        raise ValueError("target_branch is required")
    if draft is not None and not isinstance(draft, bool):
        raise ValueError("draft must be a boolean")
    resolved_reviewers = _state_or(reviewers, "reviewers")
    if resolved_reviewers is not None:
        if not isinstance(resolved_reviewers, (str, tuple, list)):
            raise ValueError("reviewers must be a comma-separated string or a list/tuple of non-empty strings")
        if isinstance(resolved_reviewers, str):
            if not any(item.strip() for item in resolved_reviewers.split(",")):
                raise ValueError("reviewers must include at least one non-empty name")
        else:
            if any(not isinstance(item, str) or not item.strip() for item in resolved_reviewers):
                raise ValueError("reviewers must be a list/tuple of non-empty strings")
            if not resolved_reviewers or any(
                not any(name.strip() for name in item.split(",")) for item in resolved_reviewers
            ):
                raise ValueError("reviewers must include at least one non-empty name")
    if dry_run is not None and not isinstance(dry_run, bool):
        raise ValueError("dry_run must be a boolean")


def _adapter_for(provider: str) -> PullRequestCreateAdapter:
    if provider == "github":
        return GitHubPullRequestCreateAdapter()
    return AzureDevOpsPullRequestCreateAdapter()


def dispatch_create_pull_request(request: PullRequestCreateRequest) -> PullRequestCreateResult:
    """Dispatch a validated request to its provider adapter."""
    return _adapter_for(request.provider).create(request)


def create_pull_request(**kwargs: Any) -> PullRequestCreateResult:
    """Create a pull request for the configured provider."""
    try:
        request = build_create_request(**kwargs)
    except Exception as exc:
        try:
            result_provider = resolve_create_provider(kwargs.get("provider"))
        except Exception:
            result_provider = "unknown"
        result = PullRequestCreateResult(False, result_provider, "invalid", error=str(exc))
    else:
        try:
            if kwargs.get("provider") is not None and _resolve_configured_provider() is None:
                set_value("platform.code_hosting", request.provider)
            result = dispatch_create_pull_request(request)
        except subprocess.TimeoutExpired as exc:
            result = PullRequestCreateResult(True, request.provider, "indeterminate", error=str(exc))
        except Exception as exc:
            result = PullRequestCreateResult(False, request.provider, "failed", error=str(exc))
    print(json.dumps(result.as_dict(), ensure_ascii=False))
    return result


def _run_request_snapshot(request_file: str, state_dir: str | None = None) -> int:
    """Load a persisted request snapshot written by ``create_pull_request_async``.

    The complete request (which may include a large PR body) is read from a
    file instead of being passed as a background-task keyword argument,
    because the background runner embeds ``func_kwargs`` directly into the
    ``python -c`` command line and large or multiline bodies could otherwise
    exceed the OS command-line length limit.
    """
    path = Path(request_file)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    finally:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            # Best-effort cleanup: a transient filesystem error here must not
            # fail a dispatch whose request JSON was already read successfully.
            pass
    if not isinstance(payload, dict):
        raise ValueError(f"request snapshot must contain a JSON object, got {type(payload).__name__}")
    if isinstance(payload.get("reviewers"), list):
        payload["reviewers"] = tuple(payload["reviewers"])
    request = PullRequestCreateRequest(**payload)
    if state_dir is None:
        result = dispatch_create_pull_request(request)
    else:
        previous_state_dir = os.environ.get("AGENTIC_DEVTOOLS_STATE_DIR")
        os.environ["AGENTIC_DEVTOOLS_STATE_DIR"] = state_dir
        try:
            result = dispatch_create_pull_request(request)
        finally:
            if previous_state_dir is None:
                os.environ.pop("AGENTIC_DEVTOOLS_STATE_DIR", None)
            else:
                os.environ["AGENTIC_DEVTOOLS_STATE_DIR"] = previous_state_dir
    print(json.dumps(result.as_dict(), ensure_ascii=False))
    return 0 if result.success else 1


def create_pull_request_async(**kwargs: Any) -> None:
    """Snapshot raw pull-request overrides and execute the request as a background task.

    An explicit ``provider`` override must match any configured
    ``platform.code_hosting``. When no provider is configured, the validated
    override is persisted to state so follow-up PR commands use the same
    provider.
    """
    # Validate required fields/provider/optional value types synchronously,
    # before persisting anything or scheduling the background task, so an
    # invalid invocation fails immediately instead of only inside
    # ``_run_request_snapshot()``.
    scheduled_state_dir = get_state_dir(create=False)
    _preflight_validate_create_request(**kwargs)
    snapshot = _build_create_request_snapshot(**kwargs)
    if kwargs.get("provider") is not None and _resolve_configured_provider() is None:
        set_value("platform.code_hosting", snapshot["provider"])
    # Persist explicit source, title, and body overrides so subsequent
    # parameterless commands and other state-based consumers can see them.
    if kwargs.get("source_branch") is not None:
        set_value("source_branch", snapshot["source_branch"])
    if kwargs.get("title") is not None:
        set_value("title", kwargs["title"])
    if kwargs.get("body") is not None:
        set_value("description", kwargs["body"])
    snapshot_payload: dict[str, Any] = {
        **snapshot,
        "reviewers": list(snapshot["reviewers"]),
    }
    snapshot_dir = scheduled_state_dir / _SNAPSHOT_DIR_NAME
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        dir=snapshot_dir,
        prefix=f"{uuid.uuid4().hex}-",
        suffix=".json",
        encoding="utf-8",
        delete=False,
    ) as handle:
        json.dump(snapshot_payload, handle, ensure_ascii=False)
        snapshot_path = Path(handle.name)
    try:
        os.chmod(snapshot_path, 0o600)
    except OSError:
        # The snapshot is created atomically via NamedTemporaryFile; this chmod
        # is only defense in depth for platforms with different temp-file modes.
        pass
    try:
        task = run_function_in_background(
            _MODULE,
            "_run_request_snapshot",
            command_display_name="agdt-create-pull-request",
            func_kwargs={"request_file": str(snapshot_path), "state_dir": str(scheduled_state_dir)},
        )
    except Exception:
        try:
            snapshot_path.unlink(missing_ok=True)
        except OSError:
            # Cleanup is best-effort; preserve the original exception if it fails.
            pass
        raise
    print_task_tracking_info(task, "Creating pull request")


def create_pull_request_async_cli() -> None:
    """CLI entry point for provider-neutral pull-request creation."""
    parser = argparse.ArgumentParser(description="Create a pull request")
    parser.add_argument(
        "--provider",
        help=(
            "Select the code-hosting provider for this PR ('azure_devops' or "
            "'github'). Must match any configured platform.code_hosting value; "
            "when unset, the selected provider is saved for follow-up commands."
        ),
    )
    parser.add_argument("--source-branch", "-b")
    parser.add_argument("--title", "-t")
    parser.add_argument("--description", "--body", "-d", "-c")
    parser.add_argument("--target-branch", "--base")
    parser.add_argument("--reviewers", "--reviewer", action="append")
    parser.add_argument("--no-draft", action="store_true")
    args = parser.parse_args()
    try:
        create_pull_request_async(
            provider=args.provider,
            source_branch=args.source_branch,
            title=args.title,
            body=args.description,
            target_branch=args.target_branch,
            draft=False if args.no_draft else None,
            reviewers=args.reviewers,
        )
    except (ValueError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
