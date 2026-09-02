"""Shared GitHub Copilot coding-agent assignment helper."""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass

from agentic_devtools.cli.ci import retry as _retry
from agentic_devtools.cli.ci.exceptions import AgentAssignmentError, ProviderRateLimitError
from agentic_devtools.cli.ci.models import COPILOT_SESSION_EVENT_STARTED
from agentic_devtools.cli.ci.retry import RetryableError, retry_with_backoff

logger = logging.getLogger(__name__)

_CODING_AGENT_API_HEADERS = {"X-GitHub-Api-Version": "2022-11-28"}
_COPILOT_ASSIGNEE_LOGIN = "copilot-swe-agent"
_COPILOT_ASSIGNEE_BOT = "copilot-swe-agent[bot]"
_COPILOT_IDENTITY_ALIASES = {
    _COPILOT_ASSIGNEE_LOGIN,
    _COPILOT_ASSIGNEE_BOT,
    "app/copilot-swe-agent",
    "copilot",
}
_AGENT_START_POLL_INITIAL_SECONDS_DEFAULT = 15
_AGENT_START_POLL_INITIAL_SECONDS_MIN = 1
_AGENT_START_POLL_INITIAL_SECONDS_MAX = 60
_AGENT_START_POLL_TIMEOUT_SECONDS_DEFAULT = 300
_AGENT_START_POLL_TIMEOUT_SECONDS_MIN = 60
_AGENT_START_POLL_TIMEOUT_SECONDS_MAX = 600
_GRAPHQL_ASSIGNMENT_HEADERS = {
    "GraphQL-Features": "issues_copilot_assignment_api_support,coding_agent_model_selection",
}


@dataclass(frozen=True)
class AgentAssignmentResult:
    """Result payload returned by :func:`assign_issue_to_agent`."""

    success: bool
    method: str
    task_id: str = ""
    task_url: str = ""
    attempts: int = 0
    token_identity: str = ""
    error: str = ""
    session_confirmed: bool = False
    outcome: str = ""


def _gh_api_call(
    endpoint: str,
    *,
    method: str = "GET",
    body: dict | None = None,
    paginate: bool = False,
    token: str | None = None,
    headers: dict[str, str] | None = None,
    response_metadata: dict[str, float | int | None] | None = None,
) -> str:
    """Proxy to ``github_provider._gh_api`` with local import to avoid cycles."""
    from agentic_devtools.cli.ci.github_provider import _gh_api

    return _gh_api(
        endpoint,
        method=method,
        body=body,
        paginate=paginate,
        token=token,
        headers=headers,
        response_metadata=response_metadata,
    )


def _validate_repo_format(repo: str) -> str | None:
    """Return normalized ``owner/repo`` if valid, else ``None``.

    Accepts an optional trailing ``.git`` suffix (stripped before validation).
    Requires exactly two non-empty segments separated by ``/``.
    """
    repo = repo.strip()
    if repo.endswith(".git"):
        repo = repo[:-4]
    parts = repo.split("/")
    if len(parts) == 2 and all(parts):
        return repo
    return None


def _resolve_assignment_token(token_env_vars: tuple[str, ...]) -> tuple[str, str]:
    for env_name in token_env_vars:
        token_value = os.environ.get(env_name, "").strip()
        if token_value:
            return env_name, token_value
    return "", ""


def _poll_coding_agent_task_started(
    *,
    repo: str,
    task_id: str,
    token: str,
    max_polls: int = 5,
) -> bool:
    """Poll the coding-agent task endpoint until ``in_progress`` status is observed.

    Returns ``True`` when the task transitions to ``in_progress``, or ``False``
    if the polling window is exhausted without observing that status.
    """
    for poll_index in range(max_polls):
        try:
            response = _gh_api_call(
                f"/repos/{repo}/copilot/coding-agent/tasks/{task_id}",
                method="GET",
                token=token,
                headers=_CODING_AGENT_API_HEADERS,
            )
            payload = json.loads(response)
        except (json.JSONDecodeError, RuntimeError):
            pass
        else:
            if str(payload.get("status") or "").strip().lower() == "in_progress":
                return True
        if poll_index < max_polls - 1:
            _retry.time.sleep(2)
    return False


def _build_assignment_instructions(
    *,
    custom_instructions: str,
    custom_agent: str | None,
    model: str | None,
    repo: str,
    base_branch: str,
) -> dict:
    assignment: dict[str, str] = {
        "target_repo": repo,
        "base_branch": base_branch,
        "custom_instructions": custom_instructions,
    }
    if custom_agent:
        assignment["custom_agent"] = custom_agent
    if model:
        assignment["model"] = model
    return {"assignees": [_COPILOT_ASSIGNEE_BOT], "agent_assignment": assignment}


def _is_bad_credentials_error(error_message: str) -> bool:
    lowered = error_message.lower()
    if "bad credentials" in lowered:
        return True
    return re.search(r"\b(?:http|status)\s*[:=]?\s*401\b", lowered) is not None


def _is_definitive_rejection(exc: BaseException) -> bool:
    """Return ``True`` if *exc* carries a non-429 HTTP 4xx rejection from GitHub.

    :func:`_gh_api` raises :class:`RuntimeError` for **any** non-retryable
    non-zero ``gh`` exit, which includes both structured HTTP 4xx responses and
    unclassified transport failures (connection reset, CLI crash, timeout).
    Only structured non-429 4xx responses embed an HTTP status code in the message;
    pure transport failures do not, so they must be treated as ambiguous.
    """
    return bool(re.search(r"\bHTTP 4(?!29)\d{2}\b", str(exc)))


def _is_explicit_http_failure(exc: BaseException) -> bool:
    """Return ``True`` when *exc* carries an explicit HTTP rejection or error.

    ``accepted_unconfirmed`` is reserved for transport ambiguity where request
    delivery itself is uncertain. Structured HTTP responses (4xx, 429, 5xx, or
    explicit rate-limit/server-error wrappers) are not ambiguous deliveries and
    must not be promoted to success when read-back is inconclusive.
    """

    pending = [exc]
    seen: set[int] = set()
    while pending:
        current = pending.pop()
        current_id = id(current)
        if current_id in seen:
            continue
        seen.add(current_id)
        if _is_definitive_rejection(current):
            return True
        message = str(current)
        lowered = message.lower()
        if "github api rate limited" in lowered or "secondary rate limit" in lowered:
            return True
        if "github api server error" in lowered:
            return True
        if re.search(r"\bHTTP 429\b", message) or re.search(r"\bHTTP 5\d{2}\b", message):
            return True
        if current.__cause__ is not None:
            pending.append(current.__cause__)
        if current.__context__ is not None:
            pending.append(current.__context__)
    return False


def _validate_assignment_token(*, token: str, token_identity: str) -> str:
    try:
        _gh_api_call("/user", method="GET", token=token)
    except RuntimeError as exc:
        message = str(exc)
        if _is_bad_credentials_error(message):
            return (
                f"Assignment token '{token_identity}' failed authentication (HTTP 401 Bad credentials). "
                "The token is likely expired, malformed, or lacks the required scopes "
                "(classic PAT needs 'repo'). Rotate the secret and retry."
            )
        raise
    return ""


def _resolve_copilot_actor_id(*, repo: str, token: str) -> str:
    from agentic_devtools.cli.ci.github_provider import (
        _credential_identity_for_token,
        _raise_for_graphql_errors,
    )

    owner, repo_name = repo.split("/", 1)
    query = """
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    suggestedActors(capabilities: [CAN_BE_ASSIGNED], first: 100) {
      nodes {
        __typename
        ... on User {
          id
          login
        }
        ... on Bot {
          id
          login
        }
      }
    }
  }
}
"""
    response_metadata: dict[str, float | int | None] = {}
    response = _gh_api_call(
        "/graphql",
        method="POST",
        body={"query": query, "variables": {"owner": owner, "repo": repo_name}},
        token=token,
        headers=_GRAPHQL_ASSIGNMENT_HEADERS,
        response_metadata=response_metadata,
    )
    payload = json.loads(response)
    retry_after_raw = response_metadata.get("retry_after")
    reset_timestamp_raw = response_metadata.get("reset_timestamp")
    remaining_raw = response_metadata.get("remaining")
    _raise_for_graphql_errors(
        payload,
        context="GitHub GraphQL error",
        provider="github",
        credential_identity=_credential_identity_for_token(token),
        retry_after=float(retry_after_raw) if isinstance(retry_after_raw, (int, float)) else None,
        reset_timestamp=float(reset_timestamp_raw) if isinstance(reset_timestamp_raw, (int, float)) else None,
        remaining=int(remaining_raw) if isinstance(remaining_raw, int) else None,
    )

    data = payload.get("data")
    if not isinstance(data, dict):
        raise RuntimeError(f"GitHub GraphQL response missing object at data (got: {type(data).__name__})")
    repository = data.get("repository")
    if not isinstance(repository, dict):
        raise RuntimeError(
            f"GitHub GraphQL response missing object at data.repository (got: {type(repository).__name__})"
        )
    suggested_actors = repository.get("suggestedActors")
    if not isinstance(suggested_actors, dict):
        raise RuntimeError(
            "GitHub GraphQL response missing object at "
            f"data.repository.suggestedActors (got: {type(suggested_actors).__name__})"
        )

    nodes = suggested_actors.get("nodes", [])
    for node in nodes if isinstance(nodes, list) else []:
        if not isinstance(node, dict):
            continue
        login = str(node.get("login", "")).strip().lower()
        if _is_copilot_identity(login):
            return str(node.get("id", "")).strip()
    return ""


def _is_copilot_identity(value: object) -> bool:
    if not isinstance(value, str):
        return False
    identity = value.strip().lower()
    if identity in _COPILOT_IDENTITY_ALIASES:
        return True
    return identity.removesuffix("[bot]") in _COPILOT_IDENTITY_ALIASES


def _assignment_state(payload: object) -> bool | None:
    if not isinstance(payload, dict):
        return None
    assignees = payload.get("assignees")
    if isinstance(assignees, list):
        saw_malformed_assignee = False
        for assignee in assignees:
            if not isinstance(assignee, dict):
                saw_malformed_assignee = True
                continue
            for key in ("login", "name", "slug", "display_login"):
                if _is_copilot_identity(assignee.get(key)):
                    return True
            for key in ("user", "bot", "app"):
                nested = assignee.get(key)
                nested_state = _assignment_state({"assignees": [nested]}) if nested is not None else False
                if nested_state is True:
                    return True
                if nested_state is None:
                    saw_malformed_assignee = True
        return None if saw_malformed_assignee else False
    if "assignee" in payload:
        assignee = payload["assignee"]
        return _assignment_state({"assignees": [assignee]}) if isinstance(assignee, dict) else None
    return None


def _is_copilot_assigned(payload: dict) -> bool:
    return _assignment_state(payload) is True


def _read_assignment_postcondition(
    *,
    repo: str,
    issue_number: int,
    token: str,
    token_identity: str,
    max_reads: int,
) -> tuple[bool | None, str]:
    """Read assignment state a bounded number of times, independent of call order."""
    last_interpretation = "not_read"
    saw_negative_read = False
    for read_number in range(1, max_reads + 1):
        try:
            response = _gh_api_call(
                f"/repos/{repo}/issues/{issue_number}",
                method="GET",
                token=token,
                headers=_CODING_AGENT_API_HEADERS,
            )
            payload = json.loads(response)
        except Exception as exc:
            last_interpretation = f"read_error:{type(exc).__name__}"
            logger.warning(
                "Issue #%d assignment read-back token_identity=%s read=%d/%d result=inconclusive error=%s",
                issue_number,
                token_identity,
                read_number,
                max_reads,
                exc,
            )
            if read_number < max_reads:
                _retry.time.sleep(min(2 ** (read_number - 1), 4))
            continue
        state = _assignment_state(payload)
        if state is True:
            return True, "copilot_assigned"
        if state is False:
            saw_negative_read = True
            last_interpretation = "copilot_not_assigned"
            if read_number < max_reads:
                _retry.time.sleep(min(2 ** (read_number - 1), 4))
            continue
        last_interpretation = "unexpected_response_shape"
        if read_number < max_reads:
            _retry.time.sleep(min(2 ** (read_number - 1), 4))
    if saw_negative_read and last_interpretation == "copilot_not_assigned":
        return False, last_interpretation
    return None, last_interpretation


def _list_issue_events(*, repo: str, issue_number: int, token: str) -> list[dict]:
    # Local import to avoid circular dependency: github_provider imports agent_assignment.
    from agentic_devtools.cli.ci.github_provider import _parse_paginated_json

    response = _gh_api_call(
        f"/repos/{repo}/issues/{issue_number}/events",
        method="GET",
        token=token,
        paginate=True,
    )
    data = _parse_paginated_json(response)
    return data if isinstance(data, list) else []


def _event_id(event: dict) -> int:
    raw_id = event.get("id")
    if isinstance(raw_id, int):
        return raw_id
    if isinstance(raw_id, str) and raw_id.isdigit():
        return int(raw_id)
    return 0


def _is_started_session_event(event: dict) -> bool:
    event_type = str(event.get("event", ""))
    return event_type == COPILOT_SESSION_EVENT_STARTED


def _parse_clamped_env_int(*, env_name: str, default: int, minimum: int, maximum: int) -> int:
    raw = os.environ.get(env_name, "").strip()
    try:
        parsed = int(raw)
    except ValueError:
        return default
    return max(minimum, min(maximum, parsed))


def _wait_for_started_session_event(
    *,
    repo: str,
    issue_number: int,
    token: str,
    baseline_event_id: int,
    initial_wait_seconds: int,
    timeout_seconds: int,
) -> dict | None:
    start = _retry.time.monotonic()
    deadline = start + float(timeout_seconds)
    next_wait = float(initial_wait_seconds)

    while True:
        remaining = deadline - _retry.time.monotonic()
        if remaining > 0:
            _retry.time.sleep(min(next_wait, remaining))

        try:
            observed_events = _list_issue_events(repo=repo, issue_number=issue_number, token=token)
        except RetryableError as exc:
            if exc.is_rate_limit:
                raise ProviderRateLimitError(
                    retry_after_seconds=exc.retry_after,
                    reset_timestamp=exc.reset_timestamp,
                    remaining=exc.remaining,
                    provider=exc.provider,
                    credential_identity=exc.credential_identity,
                    source=exc.source,
                    is_rate_limit=True,
                ) from exc
            # `_list_issue_events` calls `_gh_api_call` → `_gh_api`, which raises
            # `RetryableError` on transient server errors.  Because this poll runs
            # after the assignment POST is already confirmed, those failures must
            # remain non-fatal and must not repeat the assignment POST.
            logger.warning(
                "Error listing events for issue #%d during start-event polling "
                "(treating as session_confirmed=False): %s",
                issue_number,
                exc,
            )
            return None
        except (RuntimeError, json.JSONDecodeError) as exc:
            # `_list_issue_events` calls `_gh_api_call` → `_gh_api`, which raises
            # `RuntimeError` on other HTTP errors and `_parse_paginated_json` raises
            # `json.JSONDecodeError` on bad payloads.
            # Because this poll runs after the assignment POST is already confirmed,
            # these failures must NOT bubble up through retry_with_backoff
            # or it would re-run the assignment POST unnecessarily.
            logger.warning(
                "Error listing events for issue #%d during start-event polling "
                "(treating as session_confirmed=False): %s",
                issue_number,
                exc,
            )
            return None
        started = [
            event
            for event in observed_events
            if _is_started_session_event(event) and _event_id(event) > baseline_event_id
        ]
        if started:
            return max(started, key=_event_id)

        if _retry.time.monotonic() >= deadline:
            return None

        next_wait *= 2


def _extract_retryable_failure_message(exc: BaseException) -> str:
    if isinstance(exc, ProviderRateLimitError):
        if isinstance(exc.__cause__, RetryableError):
            cause_message = str(exc.__cause__)
            lowered = cause_message.lower()
            if "rate limit" in lowered or "http 429" in lowered or "retry-after" in lowered:
                return f"{exc}; caused by: {cause_message}"
            return cause_message
        return str(exc)
    if isinstance(exc, RuntimeError):
        return str(exc)
    return f"{type(exc).__name__}: {exc}"


def assign_issue_to_agent(
    *,
    repo: str,
    issue_number: int,
    problem_statement: str,
    custom_instructions: str = "",
    base_branch: str = "main",
    custom_agent: str | None = None,
    model: str | None = None,
    allow_preexisting_assignment: bool = True,
    token_env_vars: tuple[str, ...] = ("SPECKIT_PR_TOKEN", "COPILOT_GITHUB_TOKEN"),
    max_attempts_per_method: int = 3,
) -> AgentAssignmentResult:
    """Assign a GitHub issue to a coding agent with validated retry + fallback."""
    if max_attempts_per_method < 1:
        raise ValueError("max_attempts_per_method must be >= 1")
    if issue_number <= 0:
        raise AgentAssignmentError("issue_number must be a positive integer")
    normalized_repo = _validate_repo_format(repo)
    if normalized_repo is None:
        raise AgentAssignmentError("repo must be in 'owner/repo' format")
    repo = normalized_repo
    if not problem_statement.strip():
        raise AgentAssignmentError("problem_statement must not be empty")

    token_identity, token = _resolve_assignment_token(token_env_vars)
    if not token:
        logger.info(
            "Issue #%d assignment outcome=confirmed_failure token_identity=none response=missing_token "
            "read_back=not_read attempt=0 final_state=unassigned",
            issue_number,
        )
        return AgentAssignmentResult(
            success=False,
            method="",
            token_identity="",  # nosec B106 - placeholder identity, not a credential
            error=f"Missing assignment token. Set one of: {', '.join(token_env_vars)}",
            outcome="confirmed_failure",
        )

    logger.info(
        "Resolving agent assignment for issue #%d with token identity %s",
        issue_number,
        token_identity,
    )

    def _log_assignment_outcome(
        *,
        outcome: str,
        response: str,
        read_back: str,
        attempt: int,
        final_state: str,
    ) -> None:
        logger.info(
            "Issue #%d assignment outcome=%s token_identity=%s response=%s read_back=%s attempt=%d final_state=%s",
            issue_number,
            outcome,
            token_identity,
            response,
            read_back,
            attempt,
            final_state,
        )

    @retry_with_backoff(max_retries=max_attempts_per_method - 1)
    def _preflight_token_check() -> str:
        return _validate_assignment_token(token=token, token_identity=token_identity)

    try:
        token_error = _preflight_token_check()
    except ProviderRateLimitError:
        raise
    except (RetryableError, RuntimeError) as exc:
        token_error = f"Assignment token preflight failed for '{token_identity}': {exc}"
    if token_error:
        logger.error("Issue #%d: %s", issue_number, token_error)
        _log_assignment_outcome(
            outcome="confirmed_failure",
            response="token_preflight_failed",
            read_back="not_read",
            attempt=0,
            final_state="unassigned",
        )
        return AgentAssignmentResult(
            success=False,
            method="",
            attempts=0,
            token_identity=token_identity,
            error=token_error,
            outcome="confirmed_failure",
        )

    precheck_state, precheck_interpretation = _read_assignment_postcondition(
        repo=repo,
        issue_number=issue_number,
        token=token,
        token_identity=token_identity,
        max_reads=1,
    )
    if precheck_state is True and allow_preexisting_assignment:
        precheck_result = AgentAssignmentResult(
            success=True,
            method="agent_assignment",
            attempts=0,
            token_identity=token_identity,
            outcome="confirmed_success",
        )
        logger.info(
            "Issue #%d assignment outcome=%s token_identity=%s response=preexisting_assignment "
            "read_back=%s attempt=0 final_state=assigned",
            issue_number,
            precheck_result.outcome,
            token_identity,
            precheck_interpretation,
        )
        return precheck_result

    # The primary coding-agent tasks endpoint does not support custom_agent,
    # custom_instructions, or model.  Skip it when any of these are provided
    # and go directly to the assignee-based agent_assignment fallback,
    # which does carry those fields.
    use_primary = not (custom_agent or custom_instructions or model)
    primary_error = "skipped (custom_agent, custom_instructions, or model provided)"
    primary_attempts = 0

    if use_primary:

        @retry_with_backoff(max_retries=max_attempts_per_method - 1)
        def _copilot_actor_check() -> str:
            return _resolve_copilot_actor_id(repo=repo, token=token)

        try:
            copilot_actor_id = _copilot_actor_check()
        except ProviderRateLimitError:
            raise
        except (json.JSONDecodeError, RetryableError, RuntimeError) as exc:
            primary_error = f"skipped after Copilot actor verification failed: {exc}"
            logger.warning(
                "Issue #%d: %s; continuing to agent_assignment fallback",
                issue_number,
                primary_error,
            )
            use_primary = False
        else:
            if not copilot_actor_id:
                copilot_error = (
                    f"Copilot coding agent is not enabled for {repo} "
                    "(suggestedActors did not include copilot-swe-agent)"
                )
                logger.error("Issue #%d: %s", issue_number, copilot_error)
                _log_assignment_outcome(
                    outcome="confirmed_failure",
                    response="copilot_actor_unavailable",
                    read_back=precheck_interpretation,
                    attempt=0,
                    final_state="unassigned",
                )
                return AgentAssignmentResult(
                    success=False,
                    method="",
                    attempts=0,
                    token_identity=token_identity,
                    error=copilot_error,
                    outcome="confirmed_failure",
                )

    if use_primary:

        def _reconcile_primary_ambiguity(
            *,
            response_interpretation: str,
            inconclusive_error: str,
            task_id: str = "",
            task_url: str = "",
            accept_inconclusive_readback: bool = True,
        ) -> AgentAssignmentResult | None:
            readback_state, readback_interpretation = _read_assignment_postcondition(
                repo=repo,
                issue_number=issue_number,
                token=token,
                token_identity=token_identity,
                max_reads=min(max_attempts_per_method, 3),
            )
            if readback_state is False:
                return None
            if readback_state is None and not accept_inconclusive_readback:
                return None
            result = AgentAssignmentResult(
                success=True,
                method="coding_agent_task",
                task_id=task_id,
                task_url=task_url,
                attempts=primary_attempts,
                token_identity=token_identity,
                session_confirmed=False,
                error="" if readback_state is True else inconclusive_error,
                outcome="confirmed_success" if readback_state is True else "accepted_unconfirmed",
            )
            logger.info(
                "Issue #%d assignment outcome=%s token_identity=%s response=%s read_back=%s attempt=%d final_state=%s",
                issue_number,
                result.outcome,
                token_identity,
                response_interpretation,
                readback_interpretation,
                primary_attempts,
                "assigned" if readback_state is True else "unconfirmed",
            )
            return result

        def _reconcile_started_task_without_progress(*, task_id: str, task_url: str) -> AgentAssignmentResult:
            readback_state, readback_interpretation = _read_assignment_postcondition(
                repo=repo,
                issue_number=issue_number,
                token=token,
                token_identity=token_identity,
                max_reads=min(max_attempts_per_method, 3),
            )
            result = AgentAssignmentResult(
                success=True,
                method="coding_agent_task",
                task_id=task_id,
                task_url=task_url,
                attempts=primary_attempts,
                token_identity=token_identity,
                session_confirmed=False,
                error=(
                    ""
                    if readback_state is True
                    else (
                        f"coding-agent task {task_id!r} did not reach in_progress status within polling window, "
                        "and read-back was inconclusive."
                    )
                ),
                outcome="confirmed_success" if readback_state is True else "accepted_unconfirmed",
            )
            logger.info(
                "Issue #%d assignment outcome=%s token_identity=%s response=task_not_started read_back=%s attempt=%d "
                "final_state=%s",
                issue_number,
                result.outcome,
                token_identity,
                readback_interpretation,
                primary_attempts,
                "assigned" if readback_state is True else "unconfirmed",
            )
            return result

        def _attempt_coding_agent_task() -> AgentAssignmentResult:
            nonlocal primary_attempts
            primary_attempts += 1
            logger.info(
                "Issue #%d: coding-agent task attempt %d/%d",
                issue_number,
                primary_attempts,
                max_attempts_per_method,
            )
            try:
                response = _gh_api_call(
                    f"/repos/{repo}/copilot/coding-agent/tasks",
                    method="POST",
                    body={"problem_statement": problem_statement},
                    token=token,
                    headers=_CODING_AGENT_API_HEADERS,
                )
            except (ProviderRateLimitError, RetryableError, RuntimeError) as exc:
                result = _reconcile_primary_ambiguity(
                    response_interpretation="request_error",
                    inconclusive_error=(
                        "Coding-agent task request may have been accepted, but read-back was inconclusive."
                    ),
                    accept_inconclusive_readback=not _is_explicit_http_failure(exc),
                )
                if result is not None:
                    return result
                raise

            try:
                payload = json.loads(response)
            except json.JSONDecodeError as exc:
                result = _reconcile_primary_ambiguity(
                    response_interpretation="invalid_json",
                    inconclusive_error="Coding-agent task response JSON was invalid, but read-back was inconclusive.",
                )
                if result is not None:
                    return result
                raise RuntimeError("Invalid JSON from coding-agent task endpoint") from exc
            if not isinstance(payload, dict):
                result = _reconcile_primary_ambiguity(
                    response_interpretation="unexpected_response_shape",
                    inconclusive_error=(
                        "Coding-agent task response shape was invalid, but read-back was inconclusive."
                    ),
                )
                if result is not None:
                    return result
                raise RuntimeError("coding-agent task response must be a JSON object")

            task_id = str(payload.get("id") or "").strip()
            task_url = str(payload.get("url") or "").strip()

            if not task_id or not task_url:
                result = _reconcile_primary_ambiguity(
                    response_interpretation="missing_task_metadata",
                    inconclusive_error=(
                        "Coding-agent task response was missing required id/url, but read-back was inconclusive."
                    ),
                )
                if result is not None:
                    return result
                raise RuntimeError("coding-agent task response missing required id/url")

            if not _poll_coding_agent_task_started(repo=repo, task_id=task_id, token=token):
                return _reconcile_started_task_without_progress(
                    task_id=task_id,
                    task_url=task_url,
                )

            result = AgentAssignmentResult(
                success=True,
                method="coding_agent_task",
                task_id=task_id,
                task_url=task_url,
                attempts=primary_attempts,
                token_identity=token_identity,
                session_confirmed=True,
                outcome="confirmed_success",
            )
            _log_assignment_outcome(
                outcome="confirmed_success",
                response="task_started",
                read_back="session_started",
                attempt=primary_attempts,
                final_state="assigned",
            )
            return result

        try:
            result = _attempt_coding_agent_task()
            logger.info(
                "Issue #%d: assignment succeeded via coding-agent task (task_id=%s)",
                issue_number,
                result.task_id,
            )
            return result
        except ProviderRateLimitError:
            raise
        except (RetryableError, RuntimeError) as exc:
            primary_error = _extract_retryable_failure_message(exc)
            logger.warning("Issue #%d: coding-agent task method failed: %s", issue_number, primary_error)

    fallback_attempts = 0

    @retry_with_backoff(max_retries=max_attempts_per_method - 1)
    def _attempt_agent_assignment_post() -> AgentAssignmentResult:
        nonlocal fallback_attempts
        fallback_attempts += 1
        logger.info(
            "Issue #%d: agent_assignment assignees POST attempt %d/%d",
            issue_number,
            fallback_attempts,
            max_attempts_per_method,
        )

        try:
            existing_state, existing_interpretation = _read_assignment_postcondition(
                repo=repo,
                issue_number=issue_number,
                token=token,
                token_identity=token_identity,
                max_reads=1,
            )
            if existing_state is True and allow_preexisting_assignment:
                result = AgentAssignmentResult(
                    success=True,
                    method="agent_assignment",
                    attempts=primary_attempts + fallback_attempts,
                    token_identity=token_identity,
                    outcome="confirmed_success",
                )
                logger.info(
                    "Issue #%d assignment outcome=%s token_identity=%s response=preexisting_assignment "
                    "read_back=%s attempt=%d final_state=assigned",
                    issue_number,
                    result.outcome,
                    token_identity,
                    existing_interpretation,
                    fallback_attempts,
                )
                return result

            baseline_events = _list_issue_events(repo=repo, issue_number=issue_number, token=token)
            baseline_event_id = max((_event_id(event) for event in baseline_events), default=0)

            try:
                assignment_response = _gh_api_call(
                    f"/repos/{repo}/issues/{issue_number}/assignees",
                    method="POST",
                    body=_build_assignment_instructions(
                        custom_instructions=custom_instructions,
                        custom_agent=custom_agent,
                        model=model,
                        repo=repo,
                        base_branch=base_branch,
                    ),
                    token=token,
                    headers=_CODING_AGENT_API_HEADERS,
                )
            except ProviderRateLimitError:
                raise
            except (RetryableError, RuntimeError) as exc:
                readback_state, readback_interpretation = _read_assignment_postcondition(
                    repo=repo,
                    issue_number=issue_number,
                    token=token,
                    token_identity=token_identity,
                    max_reads=min(max_attempts_per_method, 3),
                )
                if readback_state is True:
                    result = AgentAssignmentResult(
                        success=True,
                        method="agent_assignment",
                        attempts=primary_attempts + fallback_attempts,
                        token_identity=token_identity,
                        outcome="confirmed_success",
                    )
                elif readback_state is None and not _is_explicit_http_failure(exc):
                    # Transport/rate-limit ambiguity: the POST may have reached GitHub but the
                    # response was lost.  Return accepted_unconfirmed only for transport
                    # failures whose delivery is genuinely ambiguous.  Structured HTTP 4xx/429/5xx
                    # responses must retry/fail instead of being promoted to success.
                    result = AgentAssignmentResult(
                        success=True,
                        method="agent_assignment",
                        attempts=primary_attempts + fallback_attempts,
                        token_identity=token_identity,
                        error="Assignment request may have succeeded, but read-back was inconclusive.",
                        outcome="accepted_unconfirmed",
                    )
                else:
                    failure_error = (
                        "Issue assignment request failed and read-back did not confirm Copilot assignment: "
                        f"{_extract_retryable_failure_message(exc)}"
                    )
                    if fallback_attempts < max_attempts_per_method:
                        logger.warning(
                            "Issue #%d: assignment POST response=request_error read_back=%s; retrying "
                            "agent_assignment attempt %d/%d",
                            issue_number,
                            readback_interpretation,
                            fallback_attempts,
                            max_attempts_per_method,
                        )
                        raise RetryableError(failure_error) from exc
                    result = AgentAssignmentResult(
                        success=False,
                        method="",
                        attempts=primary_attempts + fallback_attempts,
                        token_identity=token_identity,
                        error=failure_error,
                        outcome="confirmed_failure",
                    )
                logger.info(
                    "Issue #%d assignment outcome=%s token_identity=%s response=request_error read_back=%s "
                    "attempt=%d final_state=%s",
                    issue_number,
                    result.outcome,
                    token_identity,
                    readback_interpretation,
                    fallback_attempts,
                    "assigned" if readback_state is True else "unconfirmed" if readback_state is None else "unassigned",
                )
                return result
            assignment_data: dict | None = None
            try:
                assignment_data = json.loads(assignment_response)
            except json.JSONDecodeError:
                response_interpretation = "invalid_json"
                response_assigned = False
            else:
                response_assigned = _is_copilot_assigned(assignment_data)
                response_interpretation = "copilot_assigned" if response_assigned else "missing_copilot_identity"
            if not response_assigned:
                readback_state, readback_interpretation = _read_assignment_postcondition(
                    repo=repo,
                    issue_number=issue_number,
                    token=token,
                    token_identity=token_identity,
                    max_reads=min(max_attempts_per_method, 3),
                )
                if readback_state is True:
                    result = AgentAssignmentResult(
                        success=True,
                        method="agent_assignment",
                        attempts=primary_attempts + fallback_attempts,
                        token_identity=token_identity,
                        outcome="confirmed_success",
                    )
                elif readback_state is None:
                    result = AgentAssignmentResult(
                        success=True,
                        method="agent_assignment",
                        attempts=primary_attempts + fallback_attempts,
                        token_identity=token_identity,
                        error=(
                            "Assignment accepted but read-back was inconclusive; reconciliation is required."
                            if response_interpretation != "invalid_json"
                            else (
                                "Assignment response JSON was invalid, "
                                "but read-back was inconclusive; reconciliation is required."
                            )
                        ),
                        outcome="accepted_unconfirmed",
                    )
                else:
                    failure_error = (
                        "Issue assignment response did not include copilot-swe-agent[bot], "
                        "and read-back did not confirm Copilot assignment."
                        if response_interpretation != "invalid_json"
                        else ("Assignment response JSON was invalid, and read-back did not confirm Copilot assignment.")
                    )
                    if fallback_attempts < max_attempts_per_method:
                        logger.warning(
                            "Issue #%d: assignment POST response=%s read_back=%s; retrying "
                            "agent_assignment attempt %d/%d",
                            issue_number,
                            response_interpretation,
                            readback_interpretation,
                            fallback_attempts,
                            max_attempts_per_method,
                        )
                        raise RetryableError(failure_error)
                    result = AgentAssignmentResult(
                        success=False,
                        method="",
                        attempts=primary_attempts + fallback_attempts,
                        token_identity=token_identity,
                        error=failure_error,
                        outcome="confirmed_failure",
                    )
                logger.info(
                    "Issue #%d assignment outcome=%s token_identity=%s response=%s read_back=%s "
                    "attempt=%d final_state=%s",
                    issue_number,
                    result.outcome,
                    token_identity,
                    response_interpretation,
                    readback_interpretation,
                    fallback_attempts,
                    "assigned" if readback_state is True else "unconfirmed" if readback_state is None else "unassigned",
                )
                return result

            poll_initial_seconds = _parse_clamped_env_int(
                env_name="AGDT_AGENT_START_POLL_INITIAL_SECONDS",
                default=_AGENT_START_POLL_INITIAL_SECONDS_DEFAULT,
                minimum=_AGENT_START_POLL_INITIAL_SECONDS_MIN,
                maximum=_AGENT_START_POLL_INITIAL_SECONDS_MAX,
            )
            poll_timeout_seconds = _parse_clamped_env_int(
                env_name="AGDT_AGENT_START_POLL_TIMEOUT_SECONDS",
                default=_AGENT_START_POLL_TIMEOUT_SECONDS_DEFAULT,
                minimum=_AGENT_START_POLL_TIMEOUT_SECONDS_MIN,
                maximum=_AGENT_START_POLL_TIMEOUT_SECONDS_MAX,
            )

            started_event = _wait_for_started_session_event(
                repo=repo,
                issue_number=issue_number,
                token=token,
                baseline_event_id=baseline_event_id,
                initial_wait_seconds=poll_initial_seconds,
                timeout_seconds=poll_timeout_seconds,
            )
            if started_event is not None:
                result = AgentAssignmentResult(
                    success=True,
                    method="agent_assignment",
                    task_id=str(_event_id(started_event) or ""),
                    task_url=started_event.get("url") or "",
                    attempts=primary_attempts + fallback_attempts,
                    token_identity=token_identity,
                    session_confirmed=True,
                    outcome="confirmed_success",
                )
                logger.info(
                    "Issue #%d assignment outcome=%s token_identity=%s response=copilot_assigned "
                    "read_back=session_started attempt=%d final_state=assigned",
                    issue_number,
                    result.outcome,
                    token_identity,
                    fallback_attempts,
                )
                return result

            logger.warning(
                "Copilot assignment confirmed for issue #%d but no session-start event "
                "observed (poll_timeout_seconds=%d); proceeding (session_confirmed=False)",
                issue_number,
                poll_timeout_seconds,
            )
            result = AgentAssignmentResult(
                success=True,
                method="agent_assignment",
                attempts=primary_attempts + fallback_attempts,
                token_identity=token_identity,
                session_confirmed=False,
                outcome="accepted_unconfirmed",
            )
            logger.info(
                "Issue #%d assignment outcome=%s token_identity=%s response=copilot_assigned "
                "read_back=session_not_observed attempt=%d final_state=assigned",
                issue_number,
                result.outcome,
                token_identity,
                fallback_attempts,
            )
            return result
        except json.JSONDecodeError as exc:
            raise RetryableError("Invalid JSON in issue events response") from exc

    try:
        result = _attempt_agent_assignment_post()
        if result.success:
            logger.info("Issue #%d: assignment succeeded via agent_assignment fallback", issue_number)
        return result
    except ProviderRateLimitError:
        raise
    except (RetryableError, RuntimeError) as exc:
        fallback_error = _extract_retryable_failure_message(exc)
        logger.warning("Issue #%d: agent_assignment fallback failed: %s", issue_number, fallback_error)

    final_error = (
        f"All assignment methods failed. coding_agent_task: {primary_error}; agent_assignment: {fallback_error}"
    )
    logger.error("Issue #%d: %s", issue_number, final_error)
    logger.info(
        "Issue #%d assignment outcome=confirmed_failure token_identity=%s response=unavailable "
        "read_back=unconfirmed attempt=%d final_state=unassigned",
        issue_number,
        token_identity,
        fallback_attempts,
    )
    return AgentAssignmentResult(
        success=False,
        method="",
        attempts=primary_attempts + fallback_attempts,
        token_identity=token_identity,
        error=final_error,
        outcome="confirmed_failure",
    )
