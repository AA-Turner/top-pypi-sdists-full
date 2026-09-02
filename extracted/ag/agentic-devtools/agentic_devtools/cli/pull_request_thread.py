"""Provider-neutral pull-request review discussion replies."""

from __future__ import annotations

import argparse
import json
import os
import time
from collections.abc import Mapping
from typing import Any, cast

from agentic_devtools.adapters.base import (
    PullRequestThreadReplyRequest,
    PullRequestThreadReplyResult,
    is_valid_github_repository,
)
from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.config import load_platform_config
from agentic_devtools.state import get_value, load_state_locked
from agentic_devtools.task_state import print_task_tracking_info

_GRAPHQL_RESOLVE_MUTATION = """
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread { id isResolved }
  }
}
"""

_GRAPHQL_THREAD_DISCUSSION_QUERY = """
query($threadId: ID!, $after: String) {
  node(id: $threadId) {
    __typename
    ... on PullRequestReviewThread {
      pullRequest {
        number
        repository {
          nameWithOwner
        }
      }
      comments(first: 100, after: $after) {
        nodes {
          databaseId
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
}
"""


def _get_requests() -> Any:
    """Import requests lazily so dry-run and validation need no HTTP client."""
    try:
        import requests
    except ImportError as exc:  # pragma: no cover - dependency is package-required
        raise RuntimeError("The 'requests' package is required for pull-request replies") from exc
    return requests


_BOOL_TRUE = frozenset({"1", "true", "yes", "on"})
_BOOL_FALSE = frozenset({"0", "false", "no", "off"})


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


def _state_value(*keys: str, state: Mapping[str, Any] | None = None) -> object:
    if state is not None:
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
    for key in keys:
        value = get_value(key)
        if value is not None:
            return value
    return None


def _provider(provider: str | None, *, state: Mapping[str, Any] | None = None) -> str:
    selected = provider or _state_value("platform.code_hosting", "code_hosting", state=state)
    if selected is None:
        selected = load_platform_config(os.getcwd()).get("code_hosting")
    if selected not in {"azure_devops", "github"}:
        raise ValueError(
            "An explicit platform.code_hosting value is required; supported values are 'azure_devops' and 'github'"
        )
    return str(selected)


def build_reply_request(
    *,
    provider: str | None = None,
    repository: str | None = None,
    pull_request_id: str | int | None = None,
    discussion_id: str | int | None = None,
    thread_id: str | int | None = None,
    content: str | None = None,
    resolve_thread: bool | None = None,
    review_thread_id: str | None = None,
    dry_run: bool | None = None,
) -> PullRequestThreadReplyRequest:
    """Build and validate an immutable request from CLI overrides and state."""
    state = load_state_locked()
    selected_provider = _provider(provider, state=state)
    raw_pr = pull_request_id if pull_request_id is not None else _state_value("pull_request_id", state=state)
    # Choose legacy discussion-ID aliases based on the selected provider so that
    # stale provider-specific keys in state cannot cross-contaminate the request.
    if selected_provider == "azure_devops":
        _discussion_state_keys = ("discussion_id", "thread_id")
    else:
        _discussion_state_keys = ("discussion_id", "comment_id")
    raw_discussion = (
        discussion_id
        if discussion_id is not None
        else thread_id
        if thread_id is not None
        else _state_value(*_discussion_state_keys, state=state)
    )
    body = content if content is not None else _state_value("content", state=state)
    # Only fall through to the GitHub-specific alias when GitHub is the selected
    # provider; reading it for Azure DevOps can pick up a stale GitHub repo value.
    if selected_provider == "github":
        raw_repo = repository if repository is not None else _state_value("repository", "github.repo", state=state)
    else:
        raw_repo = repository if repository is not None else _state_value("repository", state=state)
    azure_context: tuple[str, str, str] | None = None
    if selected_provider == "azure_devops":
        from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig

        config: AzureDevOpsConfig | None = None
        organization = _state_value("organization", state=state)
        project = _state_value("project", state=state)
        if isinstance(organization, str) and isinstance(project, str):
            azure_context = (organization, project, raw_repo if isinstance(raw_repo, str) else "")
        else:
            config = AzureDevOpsConfig.from_state(state=state)
            azure_context = (config.organization, config.project, config.repository)
        if repository is None and not raw_repo:
            if config is None:
                config = AzureDevOpsConfig.from_state(state=state)
            raw_repo = config.repository
    if selected_provider == "github" and not raw_repo:
        from agentic_devtools.cli.github.repo_resolution import resolve_github_repo_safe

        raw_repo = resolve_github_repo_safe(state=state)
    if not isinstance(raw_repo, str) or not raw_repo.strip():
        raise ValueError("repository identity is required")
    if raw_pr is None:
        raise ValueError("pull_request_id is required")
    if raw_discussion is None:
        raise ValueError("discussion_id (or legacy thread_id) is required")
    if not isinstance(raw_pr, (str, int)) or isinstance(raw_pr, bool):
        raise ValueError("pull_request_id must be an integer")
    if not isinstance(raw_discussion, (str, int)) or isinstance(raw_discussion, bool):
        raise ValueError("discussion_id must be an integer or string")
    if not isinstance(body, str):
        raise ValueError("content is required")
    resolve = _as_bool(resolve_thread if resolve_thread is not None else _state_value("resolve_thread", state=state))
    # Only fetch the GitHub-specific review_thread_id when it can be used: the provider
    # must be GitHub and the caller must have requested resolution.  Loading it for
    # Azure DevOps or for reply-only requests would pick up stale state values and
    # fail validation or contaminate the serialized task snapshot.
    raw_review_thread: str | None = None
    if selected_provider == "github" and resolve:
        _rt_candidate: object = (
            review_thread_id
            if review_thread_id is not None
            else _state_value("review_thread_id", "github.review_thread_id", state=state)
        )
        raw_review_thread = _rt_candidate if isinstance(_rt_candidate, str) else None
    return PullRequestThreadReplyRequest(
        provider=selected_provider,  # type: ignore[arg-type]
        repository=raw_repo.strip(),
        pull_request_number=int(cast(str | int, raw_pr)),
        discussion_id=cast(str | int, raw_discussion),
        body=body,
        resolve=resolve,
        review_thread_id=raw_review_thread,
        dry_run=_as_bool(dry_run if dry_run is not None else _state_value("dry_run", state=state)),
        azure_organization=azure_context[0] if azure_context else None,
        azure_project=azure_context[1] if azure_context else None,
    )


def _sanitize_diagnostic(message: object) -> str:
    """Redact known provider credentials from a diagnostic."""
    diagnostic = str(message)
    for name in (
        "AZURE_DEV_OPS_COPILOT_PAT",
        "AZURE_DEVOPS_EXT_PAT",
        "GH_TOKEN",
        "GITHUB_TOKEN",
        "COPILOT_GITHUB_TOKEN",
    ):
        secret = os.environ.get(name)
        if secret:
            diagnostic = diagnostic.replace(secret, "[redacted]")
    return diagnostic


def _http_diagnostic(status_code: int) -> str:
    descriptions = {
        401: "authentication failed",
        403: "permission denied",
        404: "discussion or repository not found",
        409: "stale or conflicting discussion",
        422: "invalid discussion or reply payload",
        429: "rate limited after bounded automatic retries",
    }
    return descriptions.get(status_code, "provider request failed")


def _ids_match(api_value: Any, request_value: str | int) -> bool:
    """Compare discussion IDs tolerantly across int/str representations.

    GitHub returns ``in_reply_to_id`` as an integer while CLI and state
    values arrive as strings.  Normalizing both to ``int`` prevents a
    spurious miss that would allow a retry to post a duplicate reply.

    Booleans are explicitly rejected first because ``int(True) == 1`` and
    ``int(False) == 0``, which would allow a malformed API response with
    ``in_reply_to_id: true`` to match discussion ID 1.
    """
    if isinstance(api_value, bool) or isinstance(request_value, bool):
        return False
    try:
        return int(api_value) == int(request_value)
    except (TypeError, ValueError):
        return False


def _failure(request: PullRequestThreadReplyRequest, diagnostic: str) -> PullRequestThreadReplyResult:
    return PullRequestThreadReplyResult(
        provider=request.provider,
        repository=request.repository,
        pull_request_number=request.pull_request_number,
        discussion_id=request.discussion_id,
        resolution_requested=request.resolve,
        mutation_status="failed",
        resolution_status="not_attempted",
        diagnostics=(_sanitize_diagnostic(diagnostic),),
    )


def _github_token() -> str:
    for name in ("GH_TOKEN", "GITHUB_TOKEN", "COPILOT_GITHUB_TOKEN"):
        token = os.environ.get(name, "").strip()
        if token:
            return token
    raise OSError("Set GH_TOKEN, GITHUB_TOKEN, or COPILOT_GITHUB_TOKEN for GitHub replies")


def _github_reconcile_reply(
    requests: Any,
    headers: dict[str, str],
    request: PullRequestThreadReplyRequest,
    minimum_reply_id_exclusive: int | None = None,
) -> int | None:
    """Find a reply accepted before an ambiguous transport failure.

    Uses the paginated PR comments endpoint and filters by ``in_reply_to_id`` to
    avoid depending on the create-reply route which only supports POST.
    """
    page = 1
    reconciled_reply_id: int | None = None
    while True:
        comments_url = (
            f"https://api.github.com/repos/{request.repository}/pulls/"
            f"{request.pull_request_number}/comments?per_page=100&page={page}"
        )
        response = requests.get(comments_url, headers=headers, timeout=30)
        if not 200 <= response.status_code < 300:
            raise ValueError(
                "GitHub reply baseline lookup returned HTTP "
                f"{response.status_code}: {_http_diagnostic(response.status_code)}"
            )
        payload = response.json()
        if not isinstance(payload, list):
            raise ValueError("GitHub reply baseline lookup returned a malformed payload")
        for comment in payload:
            if (
                isinstance(comment, dict)
                and _ids_match(comment.get("in_reply_to_id"), request.discussion_id)
                and comment.get("body") == request.body
                and isinstance(comment.get("id"), int)
                and not isinstance(comment.get("id"), bool)
                and comment["id"] > 0
                and (minimum_reply_id_exclusive is None or comment["id"] > minimum_reply_id_exclusive)
            ):
                reconciled_reply_id = (
                    comment["id"] if reconciled_reply_id is None else max(reconciled_reply_id, comment["id"])
                )
        if len(payload) < 100:
            return reconciled_reply_id
        page += 1


def _github_validate_review_thread(
    requests: Any,
    headers: dict[str, str],
    request: PullRequestThreadReplyRequest,
) -> str | None:
    """Validate GitHub review-thread ownership and discussion membership before mutation."""
    after: str | None = None
    while True:
        response = requests.post(
            "https://api.github.com/graphql",
            headers=headers,
            json={
                "query": _GRAPHQL_THREAD_DISCUSSION_QUERY,
                "variables": {"threadId": request.review_thread_id, "after": after},
            },
            timeout=30,
        )
        if not 200 <= response.status_code < 300:
            return (
                "GitHub review-thread lookup returned HTTP "
                f"{response.status_code}: {_http_diagnostic(response.status_code)}"
            )
        payload = response.json()
        if not isinstance(payload, dict):
            return "GraphQL review-thread lookup returned a malformed payload"
        if payload.get("errors"):
            return "GraphQL review-thread lookup returned errors"

        data = payload.get("data")
        if not isinstance(data, dict):
            return "GraphQL review-thread lookup payload missing data"
        node = data.get("node")
        if not isinstance(node, dict) or node.get("__typename") != "PullRequestReviewThread":
            return "review_thread_id is not a pull-request review thread node"
        pull_request = node.get("pullRequest")
        if not isinstance(pull_request, dict):
            return "review_thread_id is missing pull-request context"
        repository = pull_request.get("repository")
        canonical_repository = repository.get("nameWithOwner") if isinstance(repository, dict) else None
        if (
            not isinstance(canonical_repository, str)
            or canonical_repository.casefold() != request.repository.casefold()
        ):
            return "review_thread_id does not belong to the configured repository"
        if pull_request.get("number") != request.pull_request_number:
            return "review_thread_id does not belong to the configured pull request"

        comments = node.get("comments")
        if not isinstance(comments, dict):
            return "review_thread_id is missing review-thread comments"
        comment_nodes = comments.get("nodes")
        if not isinstance(comment_nodes, list):
            return "review_thread comments payload is malformed"
        for comment in comment_nodes:
            if isinstance(comment, dict) and _ids_match(comment.get("databaseId"), request.discussion_id):
                return None
        page_info = comments.get("pageInfo")
        if not isinstance(page_info, dict):
            return "review_thread comments page metadata is missing"
        has_next_page = page_info.get("hasNextPage")
        if has_next_page is True:
            end_cursor = page_info.get("endCursor")
            if not isinstance(end_cursor, str) or not end_cursor:
                return "review_thread pagination cursor was missing"
            after = end_cursor
            continue
        if has_next_page is False:
            return "review_thread_id does not contain discussion_id"
        return "review_thread comments page metadata is malformed"


def _github_reply(request: PullRequestThreadReplyRequest) -> PullRequestThreadReplyResult:
    if not is_valid_github_repository(request.repository):
        return _failure(request, "GitHub repository must use owner/repo form")
    if request.resolve and request.review_thread_id is None:
        # This is intentionally checked after the reply: GitHub can still accept a
        # valid reply when the REST comment has no discoverable GraphQL thread.
        resolution_without_id = True
    else:
        resolution_without_id = False

    baseline_reply_id: int | None = None
    _baseline_ok = False
    try:
        token = _github_token()
        requests = _get_requests()
        headers = {
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        }
        try:
            baseline_reply_id = _github_reconcile_reply(requests, headers, request)
            _baseline_ok = True
        except Exception:
            pass
        if request.resolve and request.review_thread_id is not None:
            try:
                diagnostic = _github_validate_review_thread(requests, headers, request)
            except Exception as exc:
                return _failure(request, f"GitHub review-thread lookup failed: {exc}")
            if diagnostic is not None:
                return _failure(request, diagnostic)
        owner_repo = request.repository
        reply_url = (
            f"https://api.github.com/repos/{owner_repo}/pulls/"
            f"{request.pull_request_number}/comments/{request.discussion_id}/replies"
        )
        rate_limited_403 = False
        for attempt in range(3):  # pragma: no branch - each path exits on success or final retry
            response = requests.post(reply_url, headers=headers, json={"body": request.body}, timeout=30)
            response_headers = response.headers if isinstance(response.headers, Mapping) else {}
            rate_limited_403 = response.status_code == 403 and (
                "Retry-After" in response_headers
                or response_headers.get("X-RateLimit-Remaining") == "0"
                or response_headers.get("x-ratelimit-remaining") == "0"
            )
            if (response.status_code != 429 and not rate_limited_403) or attempt == 2:
                break
            retry_after = response_headers.get("Retry-After", "1")
            try:
                delay = min(float(retry_after), 10.0)
            except (TypeError, ValueError):
                delay = 1.0
            time.sleep(max(delay, 0.0))
        if not 200 <= response.status_code < 300:
            diagnostic_status_code = 429 if rate_limited_403 else response.status_code
            if 500 <= response.status_code < 600:
                if _baseline_ok:
                    try:
                        reconciled_id = _github_reconcile_reply(
                            requests,
                            headers,
                            request,
                            minimum_reply_id_exclusive=baseline_reply_id,
                        )
                    except Exception:
                        reconciled_id = None
                else:
                    reconciled_id = None
                if reconciled_id is not None:
                    reply_id = reconciled_id
                else:
                    diagnostic = (
                        f"GitHub reply returned HTTP {diagnostic_status_code}: "
                        f"{_http_diagnostic(diagnostic_status_code)}"
                    )
                    return _failure(
                        request,
                        diagnostic,
                    )
            else:
                return _failure(
                    request,
                    f"GitHub reply returned HTTP {diagnostic_status_code}: {_http_diagnostic(diagnostic_status_code)}",
                )
        else:
            payload = response.json()
            if (
                not isinstance(payload, dict)
                or not isinstance(payload.get("id"), int)
                or isinstance(payload.get("id"), bool)
                or payload["id"] <= 0
            ):
                raise ValueError("GitHub reply returned a malformed response without a valid id")
            reply_id = payload["id"]
    except Exception as exc:
        if _baseline_ok:
            try:
                reconciled_id = _github_reconcile_reply(
                    requests,
                    headers,
                    request,
                    minimum_reply_id_exclusive=baseline_reply_id,
                )
            except Exception:
                reconciled_id = None
        else:
            reconciled_id = None
        if reconciled_id is not None:
            reply_id = reconciled_id
        else:
            return _failure(request, f"GitHub reply failed: {_sanitize_diagnostic(exc)}")

    if resolution_without_id:
        return PullRequestThreadReplyResult(
            provider="github",
            repository=request.repository,
            pull_request_number=request.pull_request_number,
            discussion_id=request.discussion_id,
            resolution_requested=True,
            mutation_status="partial_success",
            reply_id=reply_id,
            resolution_status="unsupported",
            diagnostics=("GitHub review thread node ID was not supplied; reply was posted only",),
        )

    if not request.resolve:
        return PullRequestThreadReplyResult(
            provider="github",
            repository=request.repository,
            pull_request_number=request.pull_request_number,
            discussion_id=request.discussion_id,
            resolution_requested=False,
            mutation_status="replied",
            reply_id=reply_id,
            resolution_status="not_requested",
        )

    try:
        resolution_response = requests.post(
            "https://api.github.com/graphql",
            headers=headers,
            json={
                "query": _GRAPHQL_RESOLVE_MUTATION,
                "variables": {"threadId": request.review_thread_id},
            },
            timeout=30,
        )
        if not 200 <= resolution_response.status_code < 300:
            diagnostic = (
                f"GitHub review thread resolution returned HTTP {resolution_response.status_code}: "
                f"{_http_diagnostic(resolution_response.status_code)}"
            )
            return PullRequestThreadReplyResult(
                provider="github",
                repository=request.repository,
                pull_request_number=request.pull_request_number,
                discussion_id=request.discussion_id,
                resolution_requested=True,
                mutation_status="partial_success",
                reply_id=reply_id,
                resolution_status="failed",
                diagnostics=(_sanitize_diagnostic(diagnostic),),
            )
        resolution_payload = resolution_response.json()
        if resolution_payload.get("errors"):
            raise ValueError("GraphQL review thread resolution returned errors")
        resolved = resolution_payload["data"]["resolveReviewThread"]["thread"]["isResolved"]
        if not resolved:
            raise ValueError("GraphQL review thread resolution was not confirmed")
    except Exception as exc:
        return PullRequestThreadReplyResult(
            provider="github",
            repository=request.repository,
            pull_request_number=request.pull_request_number,
            discussion_id=request.discussion_id,
            resolution_requested=True,
            mutation_status="partial_success",
            reply_id=reply_id,
            resolution_status="failed",
            diagnostics=(_sanitize_diagnostic(f"GitHub thread resolution failed: {exc}"),),
        )

    return PullRequestThreadReplyResult(
        provider="github",
        repository=request.repository,
        pull_request_number=request.pull_request_number,
        discussion_id=request.discussion_id,
        resolution_requested=True,
        mutation_status="replied_and_resolved",
        reply_id=reply_id,
        resolution_status="resolved",
    )


def _azure_devops_reply(request: PullRequestThreadReplyRequest) -> PullRequestThreadReplyResult:
    try:
        from agentic_devtools.cli.azure_devops.auth import get_pat
        from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
        from agentic_devtools.tools.azure_devops import reply_to_pull_request_thread as reply

        if request.azure_organization and request.azure_project:
            config = AzureDevOpsConfig(
                organization=request.azure_organization,
                project=request.azure_project,
                repository=request.repository,
            )
        else:
            # Preserve direct-call compatibility; background requests always carry
            # the snapshotted context above.
            state_config = AzureDevOpsConfig.from_state()
            config = AzureDevOpsConfig(
                organization=state_config.organization,
                project=state_config.project,
                repository=request.repository,
            )
        # Capture the PAT once so both the reply and resolution steps use the
        # same credential (get_pat() reads from the environment at call time).
        pat = get_pat()
        # Post the reply first (without resolution) so that a resolution failure
        # can be reported as partial_success rather than swallowing the reply ID.
        result = reply(
            config=config,
            pat=pat,
            pull_request_id=request.pull_request_number,
            thread_id=int(request.discussion_id),
            content=request.body,
            resolve_thread=False,
        )
        reply_id = result["comment_id"]
        if not isinstance(reply_id, int) or isinstance(reply_id, bool) or reply_id <= 0:
            raise ValueError("Azure DevOps reply returned a malformed response without a positive comment_id")
    except Exception as exc:
        return _failure(request, f"Azure DevOps reply failed: {_sanitize_diagnostic(exc)}")

    if not request.resolve:
        return PullRequestThreadReplyResult(
            provider="azure_devops",
            repository=request.repository,
            pull_request_number=request.pull_request_number,
            discussion_id=request.discussion_id,
            resolution_requested=False,
            mutation_status="replied",
            reply_id=reply_id,
            resolution_status="not_requested",
        )

    try:
        from agentic_devtools.cli.azure_devops.auth import get_auth_headers
        from agentic_devtools.cli.azure_devops.helpers import (
            get_repository_id,
            resolve_thread_by_id,
        )

        _req = _get_requests()
        headers = get_auth_headers(pat)
        repo_id = get_repository_id(config.organization, config.project, config.repository)
        resolve_thread_by_id(
            _req,
            headers,
            config,
            repo_id,
            request.pull_request_number,
            int(request.discussion_id),
            status="fixed",
        )
    except Exception as exc:
        return PullRequestThreadReplyResult(
            provider="azure_devops",
            repository=request.repository,
            pull_request_number=request.pull_request_number,
            discussion_id=request.discussion_id,
            resolution_requested=True,
            mutation_status="partial_success",
            reply_id=reply_id,
            resolution_status="failed",
            diagnostics=(f"Reply posted but resolution failed: {_sanitize_diagnostic(exc)}",),
        )

    return PullRequestThreadReplyResult(
        provider="azure_devops",
        repository=request.repository,
        pull_request_number=request.pull_request_number,
        discussion_id=request.discussion_id,
        resolution_requested=True,
        mutation_status="replied_and_resolved",
        reply_id=reply_id,
        resolution_status="resolved",
    )


def reply_to_pull_request_thread(
    request: PullRequestThreadReplyRequest | Mapping[str, Any] | None = None,
) -> PullRequestThreadReplyResult:
    """Reply to a configured Azure DevOps or GitHub review discussion."""
    if request is None:
        request = build_reply_request()
    elif isinstance(request, Mapping):
        request = PullRequestThreadReplyRequest(**dict(request))
    if request.dry_run:
        print(
            f"[DRY RUN] Would reply to {request.provider} discussion "
            f"{request.discussion_id} on PR {request.pull_request_number}"
        )
        resolution_status = "not_requested"
        if request.resolve:
            resolution_status = (
                "unsupported"
                if (request.provider == "github" and request.review_thread_id is None)
                else "would_resolve"
            )
        return PullRequestThreadReplyResult(
            provider=request.provider,
            repository=request.repository,
            pull_request_number=request.pull_request_number,
            discussion_id=request.discussion_id,
            resolution_requested=request.resolve,
            mutation_status="dry_run",
            resolution_status=resolution_status,
            diagnostics=("No external mutation performed",),
        )
    if request.provider == "github":
        return _github_reply(request)
    return _azure_devops_reply(request)


def _reply_to_pull_request_thread_task(request: Mapping[str, Any]) -> None:
    """Execute one serialized request and persist its normalized result in the task log."""
    result = reply_to_pull_request_thread(request)
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    if result.mutation_status == "failed":
        raise RuntimeError("; ".join(result.diagnostics) or "provider mutation failed")


def reply_to_pull_request_thread_async(
    *,
    provider: str | None = None,
    repository: str | None = None,
    pull_request_id: str | int | None = None,
    discussion_id: str | int | None = None,
    thread_id: str | int | None = None,
    content: str | None = None,
    resolve_thread: bool | None = None,
    review_thread_id: str | None = None,
) -> None:
    """Capture a validated request snapshot and launch one background task."""
    request = build_reply_request(
        provider=provider,
        repository=repository,
        pull_request_id=pull_request_id,
        discussion_id=discussion_id,
        thread_id=thread_id,
        content=content,
        resolve_thread=resolve_thread,
        review_thread_id=review_thread_id,
    )
    task = run_function_in_background(
        "agentic_devtools.cli.pull_request_thread",
        "_reply_to_pull_request_thread_task",
        command_display_name="agdt-reply-to-pull-request-thread",
        args={"request": request.to_dict()},
        func_kwargs={"request": request.to_dict()},
    )
    print_task_tracking_info(task, "Replying to pull request thread")


def reply_to_pull_request_thread_async_cli() -> None:  # pragma: no cover
    """CLI entry point for the provider-neutral background command."""
    parser = argparse.ArgumentParser(description="Reply to a pull request thread (async)")
    parser.add_argument("--provider")
    parser.add_argument("--repository", "--repo")
    parser.add_argument("--pull-request-id", "-p")
    parser.add_argument("--discussion-id", "--thread-id", "-t")
    parser.add_argument("--content", "-c")
    parser.add_argument("--review-thread-id")
    parser.add_argument("--resolve-thread", action=argparse.BooleanOptionalAction, default=None)
    args = parser.parse_args()
    reply_to_pull_request_thread_async(
        provider=args.provider,
        repository=args.repository,
        pull_request_id=args.pull_request_id,
        discussion_id=args.discussion_id,
        content=args.content,
        resolve_thread=args.resolve_thread,
        review_thread_id=args.review_thread_id,
    )
