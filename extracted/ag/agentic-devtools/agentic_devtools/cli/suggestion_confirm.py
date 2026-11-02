"""CLI command for confirming addressed pull-request suggestions."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from typing import Any, Literal, cast

from agentic_devtools.adapters.suggestion_confirm import (
    SuggestionConfirmationAdapter,
    SuggestionConfirmationRequest,
)
from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.pull_request_comments import _resolve_repository, resolve_comment_provider
from agentic_devtools.state import load_state_locked
from agentic_devtools.task_state import print_task_tracking_info

_MODULE = "agentic_devtools.cli.suggestion_confirm"

_BOOL_TRUE = frozenset({"1", "true", "yes", "on"})
_BOOL_FALSE = frozenset({"0", "false", "no", "off"})


def _positive_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError(f"{name} must be a positive integer")
    try:
        number = int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a positive integer") from exc
    if number <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return number


def _as_bool(value: object, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    normalised = str(value).lower()
    if normalised in _BOOL_TRUE:
        return True
    if normalised in _BOOL_FALSE:
        return False
    raise ValueError(f"Unrecognised boolean value {value!r}. Use one of: true/false, yes/no, 1/0, on/off.")


def _state_value(state: Mapping[str, Any], *keys: str) -> object:
    """Resolve the first matching key from one immutable state snapshot."""
    for key in keys:
        current: object = state
        for part in key.split("."):
            if not isinstance(current, Mapping) or part not in current:
                current = None
                break
            current = current[part]
        if current is not None:
            return current
    return None


def build_confirmation_request(
    *,
    provider: str | None = None,
    repository: str | None = None,
    pull_request_id: str | int | None = None,
    discussion_id: str | int | None = None,
    commit_hash: str | None = None,
    review_thread_id: str | None = None,
    dry_run: bool | None = None,
    organization: str | None = None,
    project: str | None = None,
) -> SuggestionConfirmationRequest:
    """Resolve one immutable state snapshot and CLI values into a validated request."""
    state = load_state_locked()

    def _lookup(key: str) -> object | None:
        return _state_value(state, key)

    selected = resolve_comment_provider(provider, state_lookup=_lookup)
    pr_raw = pull_request_id if pull_request_id is not None else _state_value(state, "pull_request_id")
    discussion_raw: object
    if discussion_id is not None:
        discussion_raw = discussion_id
    elif selected == "github":
        discussion_raw = _state_value(state, "discussion_id", "github.comment_id", "comment_id")
    else:
        discussion_raw = _state_value(state, "discussion_id", "thread_id")
    commit = commit_hash if commit_hash is not None else _state_value(state, "suggestion.commit_hash")
    if not isinstance(commit, str) or not commit.strip():
        raise ValueError("suggestion.commit_hash is required")
    repo = _resolve_repository(selected, repository, state_lookup=_lookup, state=state)
    thread = review_thread_id
    if thread is None and selected == "github":
        thread = cast("str | None", _state_value(state, "review_thread_id", "github.review_thread_id"))
    azure_organization = organization
    azure_project = project
    if selected == "azure_devops" and (azure_organization is None or azure_project is None):
        config = AzureDevOpsConfig.from_state(state=state)
        if azure_organization is None:
            azure_organization = config.organization
        if azure_project is None:
            azure_project = config.project
    return SuggestionConfirmationRequest(
        provider=cast(Literal["azure_devops", "github"], selected),
        repository=repo,
        pull_request_id=_positive_int(pr_raw, "pull_request_id"),
        discussion_id=_positive_int(discussion_raw, "discussion_id"),
        commit_hash=commit,
        review_thread_id=thread,
        dry_run=_as_bool(dry_run if dry_run is not None else _state_value(state, "dry_run")),
        organization=azure_organization,
        project=azure_project,
    )


def _invalid_result(exc: Exception) -> dict[str, object]:
    """Build the normalized ``invalid`` payload for a validation failure."""
    return {
        "success": False,
        "provider": "unknown",
        "status": "invalid",
        "reply_id": None,
        "diagnostics": [str(exc)[:1000]],
    }


def confirm_suggestion_addressed(
    request: SuggestionConfirmationRequest | dict[str, Any] | None = None,
) -> dict[str, object]:
    """Confirm a suggestion synchronously and print its normalized result."""
    result_payload: dict[str, object]
    try:
        if request is None:
            built = build_confirmation_request()
        elif isinstance(request, dict):
            built = SuggestionConfirmationRequest(**request)
        else:
            built = request
        result = SuggestionConfirmationAdapter().confirm(built)
    except Exception as exc:
        result_payload = _invalid_result(exc)
    else:
        result_payload = result.as_dict()
    print(json.dumps(result_payload, ensure_ascii=False))
    return result_payload


def _confirmation_task(**kwargs: Any) -> int:  # pragma: no cover
    result = confirm_suggestion_addressed(kwargs.get("request"))
    return 0 if result["success"] else 1


def confirm_suggestion_addressed_async(
    pull_request_id: str | None = None,
    thread_id: str | None = None,
    commit_hash: str | None = None,
    provider: str | None = None,
    repository: str | None = None,
    review_thread_id: str | None = None,
) -> None:
    """Validate a suggestion confirmation and execute it in the background."""
    try:
        request = build_confirmation_request(
            provider=provider,
            repository=repository,
            pull_request_id=pull_request_id,
            discussion_id=thread_id,
            commit_hash=commit_hash,
            review_thread_id=review_thread_id,
        )
    except Exception as exc:
        print(json.dumps(_invalid_result(exc), ensure_ascii=False))
        sys.exit(1)
    task = run_function_in_background(
        _MODULE,
        "_confirmation_task",
        command_display_name="agdt-confirm-suggestion-addressed",
        args={"request": request.__dict__},
        func_kwargs={"request": request.__dict__},
    )
    print_task_tracking_info(task, "Confirming suggestion addressed")


def confirm_suggestion_addressed_async_cli() -> None:  # pragma: no cover
    """Parse command-line options and start confirmation in the background."""
    parser = argparse.ArgumentParser(description="Confirm a suggestion was addressed")
    parser.add_argument("-p", "--pull-request-id")
    parser.add_argument("-t", "--thread-id")
    parser.add_argument("-c", "--commit-hash")
    parser.add_argument("--provider")
    parser.add_argument("--repository", "--repo", dest="repository")
    parser.add_argument("--review-thread-id")
    args = parser.parse_args()
    confirm_suggestion_addressed_async(**vars(args))


__all__ = [
    "build_confirmation_request",
    "confirm_suggestion_addressed",
    "confirm_suggestion_addressed_async",
    "confirm_suggestion_addressed_async_cli",
]
